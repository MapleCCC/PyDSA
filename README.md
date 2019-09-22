# PySTL

A toy project dedicated to study purpose. Learn both Python programming language and the subject of data structures and algorithms via practice process of re-inventing wheels. Code here is not intended for production environment or any pragmatic usage. Personal reuse purpose.

## How to use

1. Pick the data structure you need from [Table](#table). Copy source code or individual file.

2. Add the `algorithms/` package to your working directory.

3. Deploy the `algorithms/` directory to somewhere centric, add it to `PYTHONPATH`.

## Table

[......]

## Run Test

The repo uses [`hypothesis`](https://github.com/HypothesisWorks/hypothesis) to test. Install it before running unit tests.

```bash
# Install prerequisites
$ pip install -r test_requirements.txt

# Run all test suites
$ make test

# Run a specific test
$ python -m unittest test.test_splay_tree
```
