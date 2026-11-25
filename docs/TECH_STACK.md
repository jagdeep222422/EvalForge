# EvalForge: technology stack

## Language and runtime
- Python 3.12 (Ubuntu) for the pipeline, grader and tests

## Test and validation
- pytest: runs the feature and regression tests
- Harbor 0.25.0: packages each task and runs the nop and oracle checks
- Docker and Docker Compose: build and run each task's container

## Base project
- pallets/click 8.5.1: the open-source Python library the tasks extend

## Build and version control
- Git and GitHub: source control and submission
- Bash scripts: `solve.sh` (oracle solution) and `test.sh` (verifier entry point)
- Ubuntu 24.04: base image inside each task container

## AI assistance
- Claude (Anthropic): used during development as a coding assistant. The pipeline does not call an AI model yet.
