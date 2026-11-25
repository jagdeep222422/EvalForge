#!/usr/bin/env python3
"""EvalForge task factory: validate candidate features and package the accepted ones as Harbor tasks.

Usage:
  python pipeline.py --repo <clone of pallets/click> --python <venv python> \
      --candidates <dir of candidate dirs> --out tasks/ [--report report.json]

Each candidate dir follows the layout documented in validate.py. Accepted candidates are written to
<out>/<name>/ with instruction.md, solution/solution.patch, tests/, environment/Dockerfile and task.toml.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys

import validate

HERE = pathlib.Path(__file__).resolve().parent
TEMPLATES = HERE / "templates"
BASE_TAG = "8.5.1"
BASE_COMMIT = "cf19179e8e2fd54c601378cec9e0d21bb12b6fb1"
AUTHOR = "Jagdeep Kumar Mahto"


def package(cand_dir: pathlib.Path, out_dir: pathlib.Path, meta: dict, regression: list[str]) -> pathlib.Path:
    dst = out_dir / meta["name"]
    (dst / "solution").mkdir(parents=True, exist_ok=True)
    (dst / "tests").mkdir(parents=True, exist_ok=True)
    (dst / "environment").mkdir(parents=True, exist_ok=True)

    shutil.copy(cand_dir / "instruction.md", dst / "instruction.md")
    shutil.copy(cand_dir / "solution.patch", dst / "solution" / "solution.patch")
    for name in meta["test_files"]:
        shutil.copy(cand_dir / "tests" / name, dst / "tests" / name)

    (dst / "tests" / "fail_to_pass.json").write_text(json.dumps(meta["feature_tests"], indent=2) + "\n")
    (dst / "tests" / "pass_to_pass.json").write_text(json.dumps(regression, indent=2) + "\n")
    shutil.copy(TEMPLATES / "grade.py", dst / "tests" / "grade.py")
    shutil.copy(TEMPLATES / "tests.Dockerfile", dst / "tests" / "Dockerfile")
    (dst / "tests" / "test.sh").write_text(
        "#!/bin/bash\n# Harbor verifier entry point. Writes the reward to /logs/verifier/reward.txt.\n"
        "set -u\n"
        + "".join(f"cp /tests/{n} /app/tests/{n}\n" for n in meta["test_files"])
        + "python3 /tests/grade.py\n"
    )
    (dst / "tests" / "test.sh").chmod(0o755)
    shutil.copy(TEMPLATES / "environment.Dockerfile", dst / "environment" / "Dockerfile")

    toml = (TEMPLATES / "task.toml").read_text()
    toml = toml.replace("click-string-length", meta["name"])
    toml = toml.replace("Add a length-limited StringLength parameter type to pallets/click.", meta["description"])
    toml = toml.replace("cf19179e8e2fd54c601378cec9e0d21bb12b6fb1", BASE_COMMIT)
    toml = toml.replace('authors = ["Jagdeep Kumar Mahto"]', f'authors = ["{AUTHOR}"]')
    (dst / "task.toml").write_text(toml)

    (dst / "README.md").write_text(
        f"# {meta['name']}\n\n{meta['description']}\n\n"
        f"Base: pallets/click tag {BASE_TAG} (`{BASE_COMMIT}`).\n\n"
        f"- `tests/fail_to_pass.json`: {len(meta['feature_tests'])} feature tests\n"
        f"- `tests/pass_to_pass.json`: {len(regression)} regression tests\n"
    )
    return dst


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="local clone of pallets/click")
    ap.add_argument("--python", required=True, help="python with click's test dependencies installed")
    ap.add_argument("--candidates", required=True, help="directory containing candidate dirs")
    ap.add_argument("--out", required=True, help="directory to write accepted task folders")
    ap.add_argument("--report", default="pipeline_report.json")
    ap.add_argument("--workdir", default="/tmp/evalforge-work")
    args = ap.parse_args()

    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    work = pathlib.Path(args.workdir)
    work.mkdir(parents=True, exist_ok=True)

    print("Computing regression baseline at base commit...")
    regression = validate.baseline_regression(args.repo, BASE_COMMIT, args.python, str(work / "baseline"))
    print(f"  {len(regression)} regression tests pass at base")

    accepted_sets = validate.accepted_identifier_sets(
        [p for p in out_dir.iterdir() if p.is_dir()]
    )
    report = []
    for cand in sorted(pathlib.Path(args.candidates).iterdir()):
        if not (cand / "candidate.json").exists():
            continue
        meta = json.loads((cand / "candidate.json").read_text())
        ok, reason, ids = validate.validate(
            cand, args.repo, BASE_COMMIT, args.python, regression, accepted_sets
        )
        print(f"[{'ACCEPT' if ok else 'REJECT'}] {meta['name']}: {reason}")
        report.append({"name": meta["name"], "accepted": ok, "reason": reason})
        if ok:
            package(cand, out_dir, meta, regression)
            accepted_sets.append(ids)

    pathlib.Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
    accepted = sum(1 for r in report if r["accepted"])
    print(f"\n{accepted}/{len(report)} candidates accepted. Report: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
