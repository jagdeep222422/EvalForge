"""Compute the reward from the feature and regression test lists.

Rules: any regression failure -> 0.0; all feature tests pass -> 1.0;
otherwise the share of feature tests that pass.
"""
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("VERIFIER_OUT", "/logs/verifier")


def run(ids, label):
    if not ids:
        return {}
    xml_path = os.path.join(OUT, f"{label}.xml")
    subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         f"--junitxml={xml_path}", *ids],
        cwd=os.environ.get("REPO", "/app"),
        env=dict(os.environ, PYTHONPATH=os.path.join(os.environ.get("REPO", "/app"), "src")),
    )
    results = {}
    if not os.path.exists(xml_path):
        return {i: False for i in ids}
    for tc in ET.parse(xml_path).getroot().iter("testcase"):
        ok = not any(c.tag in ("failure", "error", "skipped") for c in tc)
        results[tc.get("classname", "") + "::" + tc.get("name", "")] = ok
    return results


def main():
    os.makedirs(OUT, exist_ok=True)
    feature = json.load(open(os.path.join(HERE, "fail_to_pass.json")))
    regression = json.load(open(os.path.join(HERE, "pass_to_pass.json")))
    f_ok = sum(1 for i in feature if (r := run([i], "f")) and all(r.values()))
    reg_res = run(regression, "regression")
    regression_failed = any(not v for v in reg_res.values()) or len(reg_res) < len(regression)
    reward = 0.0 if regression_failed else (f_ok / len(feature))
    open(os.path.join(OUT, "reward.txt"), "w").write(str(reward))
    print(f"feature {f_ok}/{len(feature)}, regression_failed={regression_failed}, reward={reward}")


if __name__ == "__main__":
    main()
