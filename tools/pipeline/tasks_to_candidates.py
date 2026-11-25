"""Convert existing task folders into candidate folders (used to replay known-good work)."""
import json, pathlib, shutil, sys

src_root, dst_root = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
for task in sorted(p for p in src_root.iterdir() if p.is_dir()):
    toml = (task / "task.toml").read_text()
    desc = next(l.split("=", 1)[1].strip().strip('"') for l in toml.splitlines() if l.startswith("description"))
    name = task.name
    cand = dst_root / name
    (cand / "tests").mkdir(parents=True, exist_ok=True)
    test_files = [p.name for p in (task / "tests").glob("test_*.py")]
    for t in test_files:
        shutil.copy(task / "tests" / t, cand / "tests" / t)
    shutil.copy(task / "instruction.md", cand / "instruction.md")
    shutil.copy(task / "solution" / "solution.patch", cand / "solution.patch")
    meta = {"name": name, "description": desc,
            "feature_tests": json.loads((task / "tests" / "fail_to_pass.json").read_text()),
            "test_files": test_files}
    (cand / "candidate.json").write_text(json.dumps(meta, indent=2))
    print("candidate", name, len(meta["feature_tests"]), "feature tests")
