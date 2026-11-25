"""Automated validation of Track 1 candidates against pallets/click.

A candidate is a directory:
  candidate.json   {"name", "description", "feature_tests": [nodeid...], "test_files": [name...]}
  instruction.md   requirement text shown to the AI under test
  solution.patch   reference implementation (git diff against the base commit)
  tests/           test files named in test_files

Checks (mirror the Harbor nop/oracle matrix described in the spec):
  nop    feature tests must FAIL on the base commit; regression tests must PASS
  oracle feature tests and regression tests must all PASS with the patch applied
  distinct the task's identifiers must not heavily overlap an accepted task
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import tempfile

PYTEST_ARGS = ["-m", "pytest", "-rA", "-q", "--tb=no", "-p", "no:cacheprovider"]
STATUS_LINE = re.compile(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS) (.+)$")


def sh(args, cwd=None, env=None, check=False):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, check=check)


def collect_ids(workdir, python, env):
    """Exact node IDs pytest collects in workdir (one per line, unambiguous)."""
    out = sh([python, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider"],
             cwd=workdir, env=env).stdout
    return [l for l in out.splitlines() if "::" in l]


def pytest_results(workdir, python, env, nodeids=None, known_ids=None):
    """Return {nodeid: status} from pytest's -rA summary.

    Status lines look like "PASSED <nodeid>" or "PASSED <nodeid> - <message>". Splitting on
    " - " is unsafe because parametrized IDs can contain it, so each line is matched against
    the exact collected IDs instead.
    """
    cmd = [python, *PYTEST_ARGS] + (list(nodeids) if nodeids else [])
    out = sh(cmd, cwd=workdir, env=env).stdout
    ids = set(known_ids) if known_ids is not None else set(collect_ids(workdir, python, env))
    results = {}
    for line in out.splitlines():
        m = STATUS_LINE.match(line.strip())
        if not m:
            continue
        status, rest = m.group(1), m.group(2)
        if rest in ids:
            results[rest] = status
            continue
        for nid in ids:
            if rest.startswith(nid + " - "):
                results[nid] = status
                break
    return results


class Workspace:
    """A detached git worktree of the base commit, using the worktree's own click source."""

    def __init__(self, repo, commit, python, root):
        self.path = pathlib.Path(root) / "wt"
        sh(["git", "-C", repo, "worktree", "add", "--detach", str(self.path), commit], check=True)
        self.repo = repo
        self.python = python
        self.env = dict(os.environ, PYTHONPATH=str(self.path / "src"))
        probe = sh([python, "-c", "import click,sys;print(click.__file__)"], cwd=self.path, env=self.env)
        assert str(self.path) in probe.stdout, f"click not imported from worktree: {probe.stdout}"

    def run(self, nodeids=None):
        return pytest_results(self.path, self.python, self.env, nodeids)

    def all_ids(self):
        return collect_ids(self.path, self.python, self.env)

    def apply(self, patch_file):
        check = sh(["git", "-C", str(self.path), "apply", "--check", str(patch_file)])
        if check.returncode != 0:
            return False, check.stderr.strip()
        sh(["git", "-C", str(self.path), "apply", str(patch_file)], check=True)
        return True, ""

    def install_tests(self, cand_dir, test_files):
        for name in test_files:
            dst = self.path / "tests" / name
            dst.write_text((pathlib.Path(cand_dir) / "tests" / name).read_text())

    def close(self):
        sh(["git", "-C", self.repo, "worktree", "remove", "--force", str(self.path)])


def baseline_regression(repo, commit, python, root):
    """Ids of tests that pass at the base commit (the pass_to_pass list)."""
    ws = Workspace(repo, commit, python, root)
    try:
        res = ws.run(ws.all_ids())
        return sorted(k for k, v in res.items() if v == "PASSED")
    finally:
        ws.close()


def identifiers(patch_text):
    """Identifiers added by a patch, used to measure how distinct two tasks are."""
    added = [l[1:] for l in patch_text.splitlines() if l.startswith("+") and not l.startswith("+++")]
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{3,}", "\n".join(added)))


def is_distinct(ids, accepted_ids, threshold=0.6):
    for other in accepted_ids:
        if not ids or not other:
            continue
        jaccard = len(ids & other) / len(ids | other)
        if jaccard >= threshold:
            return False
    return True


def validate(cand_dir, repo, commit, python, regression, accepted_ids):
    """Return (accepted: bool, reason: str, ids: set)."""
    cand = pathlib.Path(cand_dir)
    meta = json.loads((cand / "candidate.json").read_text())
    feature = meta["feature_tests"]
    patch_text = (cand / "solution.patch").read_text()
    ids = identifiers(patch_text)

    if not is_distinct(ids, accepted_ids):
        return False, "too similar to an accepted task", ids

    with tempfile.TemporaryDirectory() as root:
        ws = Workspace(repo, commit, python, root)
        try:
            ws.install_tests(cand, meta["test_files"])

            nop = ws.run(feature)
            passing_on_base = [f for f in feature if nop.get(f) == "PASSED"]
            if passing_on_base:
                return False, f"feature tests already pass on base: {passing_on_base[:3]}", ids

            ok, err = ws.apply(cand / "solution.patch")
            if not ok:
                return False, f"patch does not apply: {err[:200]}", ids

            oracle = ws.run(feature + regression)
            failed_feature = [f for f in feature if oracle.get(f) != "PASSED"]
            if failed_feature:
                return False, f"oracle fails feature tests: {failed_feature[:3]}", ids
            failed_reg = [r for r in regression if oracle.get(r) != "PASSED"]
            if failed_reg:
                return False, f"patch breaks {len(failed_reg)} regression tests: {failed_reg[:3]}", ids
            return True, "accepted", ids
        finally:
            ws.close()


def accepted_identifier_sets(task_dirs):
    sets = []
    for d in task_dirs:
        p = pathlib.Path(d) / "solution" / "solution.patch"
        if p.exists():
            sets.append(identifiers(p.read_text()))
    return sets
