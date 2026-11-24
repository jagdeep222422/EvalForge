# Mutation test results

Each reference patch was broken on purpose (one mutant per line) and the feature tests were run against it. KILLED means at least one test failed, as required.

```
error: pathspec 'src' did not match any file(s) known to git
Traceback (most recent call last):
  File "/tmp/claude-0/mutate.py", line 39, in <module>
    print(f"{task} mutant {i+1}: {run(task,i)}")
                                  ~~~^^^^^^^^
  File "/tmp/claude-0/mutate.py", line 23, in run
    subprocess.run(["git","checkout","-q","--","src"],check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.13/subprocess.py", line 578, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['git', 'checkout', '-q', '--', 'src']' returned non-zero exit status 1.
```
