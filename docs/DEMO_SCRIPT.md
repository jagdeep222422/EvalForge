# Walkthrough video script (about 3 minutes)

Record the screen with OBS (free) or your phone. Show a terminal, the GitHub repo, and the results file.
Read the bold lines aloud or put them as on-screen captions.

## 0:00 to 0:20. Introduction
- Show the repo page: https://github.com/jagdeep222422/EvalForge
- Say: **"EvalForge turns real codebases into verified coding tasks for testing AI. This is my Track 1 entry, built on pallets/click."**

## 0:20 to 0:45. The tasks
- Run: `ls tasks`
- Say: **"There are five tasks, each adding a different click feature. Each one is a Harbor task folder: instructions, a reference solution, and tests."**
- Open `tasks/click-string-length/instruction.md` and read the first requirement.

## 0:45 to 1:30. The two checks
- Run the nop check and show the 0.0 result:
  `harbor run -p tasks/click-string-length -a nop -k 1 -o runs/nop-demo --no-delete -y`
- Say: **"With no change, the feature tests fail, so the reward is 0. That is the correct behaviour."**
- Run the oracle check and show the 1.0 result:
  `harbor run -p tasks/click-string-length -a oracle -k 1 -o runs/oracle-demo --no-delete -y`
- Say: **"With the reference fix applied, every feature test and all 2,434 existing tests pass, so the reward is 1."**
- Show `docs/HARBOR_RESULTS.md` with all five tasks.

## 1:30 to 2:15. Proof the tests are meaningful
- Open `docs/MUTATION_RESULTS.md`.
- Say: **"I broke each reference change in several ways on purpose. The tests caught every one."**

## 2:15 to 2:50. The validation pipeline
- Show `tools/pipeline/README.md`.
- Say: **"The pipeline checks each candidate feature for distinctness, the nop and oracle behaviour, and that no existing test breaks. In my tests it accepted all five good tasks and rejected four bad ones."**
- Be clear that the model-based generator is not built yet. Say: **"The next step is adding a model that proposes new features. That step is not built yet."**

## 2:50 to 3:00. Close
- Show `docs/TECHNICAL_WRITEUP.md`.
- Say: **"Thank you. The write-up covers the design, the tools used and the limits."**

## Before you record
- Run each command once beforehand so the output is ready.
- Keep the terminal font large enough to read on a phone.
- Do not show your API key or any password on screen.
