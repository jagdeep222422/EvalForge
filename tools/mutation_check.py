import subprocess, sys, pathlib
PY="/tmp/claude-0/click-venv/bin/python"; PYTEST="/tmp/claude-0/click-venv/bin/pytest"
TASKS="/home/claude/evalforge/tasks"
MUTANTS = {
 "click-string-length": ("src/click/types.py", [
   ("if self.min_length is not None and length < self.min_length:", "if self.min_length is not None and length <= self.min_length:"),
   ("if self.max_length is not None and length > self.max_length:", "if self.max_length is not None and length >= self.max_length:")]),
 "click-choice-prefix": ("src/click/types.py", [
   ("if self.allow_prefix and normed_value:", "if self.allow_prefix:"),
   ("if len(matches) > 1:", "if len(matches) > 2:")]),
 "click-path-suffix": ("src/click/types.py", [
   ("if not is_dash and self.allowed_suffixes is not None:", "if False:"),
   ("if not os.fspath(value).endswith(self.allowed_suffixes):", "if not os.fspath(value).endswith(self.allowed_suffixes[:1]):")]),
 "click-group-alias": ("src/click/core.py", [
   ("        if cmd_name in self.commands:\n            return self.commands[cmd_name]\n\n        target = self.aliases.get(cmd_name)",
    "        target = self.aliases.get(cmd_name)\n        if target is not None:\n            return self.commands.get(target)\n        if cmd_name in self.commands:\n            return self.commands[cmd_name]\n\n        target = self.aliases.get(cmd_name)"),
   ("        return self.commands.get(target)", "        return self.commands.get(cmd_name)")]),
 "click-help-metavar": ("src/click/core.py", [
   ("if not self.is_flag and not self.count and self.show_metavar:", "if not self.is_flag and not self.count:")]),
}
def run(task, mut_idx):
    path, muts = MUTANTS[task]
    subprocess.run(["git","checkout","-q","--","src"],check=True)
    subprocess.run(["git","apply",f"{TASKS}/{task}/solution/solution.patch"],check=True)
    src = pathlib.Path(path); text = src.read_text()
    old, new = muts[mut_idx]
    if old not in text: return "SKIP (pattern not found)"
    src.write_text(text.replace(old, new, 1))
    tests = pathlib.Path(f"{TASKS}/{task}/tests")
    testfile = next(p for p in tests.glob("test_*.py"))
    pathlib.Path("tests", testfile.name).write_text(testfile.read_text())
    r = subprocess.run([PYTEST,"-q","-p","no:cacheprovider",f"tests/{testfile.name}"],capture_output=True,text=True)
    pathlib.Path("tests", testfile.name).unlink()
    subprocess.run(["git","checkout","-q","--","src"],check=True)
    last = r.stdout.strip().splitlines()[-1]
    return ("KILLED" if r.returncode!=0 else "SURVIVED") + "  " + last
for task,(path,muts) in MUTANTS.items():
    for i in range(len(muts)):
        print(f"{task} mutant {i+1}: {run(task,i)}")
subprocess.run(["git","checkout","-q","--","src"]); print("tree clean:", subprocess.run(["git","status","--porcelain"],capture_output=True,text=True).stdout.strip()=="")
