# play

A Python workspace for learning Python and practicing LeetCode problems to keep coding skills sharp. Designed to grow into Pandas and machine-learning work.

## Toolchain

| Tool   | Purpose                              | Pinned in                |
| ------ | ------------------------------------ | ------------------------ |
| mise   | Manages Python and uv versions       | `mise.toml`              |
| uv     | Dependency resolution + virtual env  | `mise.toml` + `uv.lock`  |
| ruff   | Linting and formatting (dev dep)     | `pyproject.toml`         |
| pytest | Test runner (dev dep)                | `pyproject.toml`         |

Python `3.13.13` and uv `0.11.8` are pinned in `mise.toml`. When you `cd` into the repo, mise activates them automatically (assuming mise is hooked into your shell). The `_.python.venv` setting in `mise.toml` also activates `.venv/` so `python`, `pytest`, `ruff` etc. resolve to the project's venv without needing `source .venv/bin/activate`.

`UV_PYTHON_PREFERENCE = "only-system"` tells uv to use mise's Python rather than downloading its own — one source of truth for the interpreter version.

## First-time setup

```sh
mise trust .       # one-time: trust the mise.toml in this repo
mise install       # install pinned Python + uv
uv sync            # create .venv and install dev deps from uv.lock
```

## Daily workflow

```sh
uv run python main.py       # run a script
uv run pytest               # run tests
uv run pytest -k two_sum    # run a specific test
uv run ruff check .         # lint
uv run ruff format .        # format
uv add <package>            # add a runtime dep (updates pyproject.toml + uv.lock)
uv add --dev <package>      # add a dev-only dep
uv lock --upgrade           # bump locked versions
```

`uv run` makes sure the command runs against this project's `.venv`. You don't need to activate the venv manually.

## Project layout

```
.
├── leetcode/        # one module per LeetCode problem (e.g. two_sum.py)
├── tests/           # pytest tests, mirroring leetcode/ filenames
├── notebooks/       # scratch Jupyter notebooks for exploring (Pandas, ML, etc.)
├── main.py          # entry-point scratchpad
├── mise.toml        # pinned Python + uv versions
├── pyproject.toml   # project metadata, dependencies, ruff + pytest config
└── uv.lock          # locked dependency versions (commit this)
```

`leetcode/two_sum.py` and `tests/test_two_sum.py` are an example pair showing the convention: each problem gets a module with a `Solution` class, and a parametrised pytest file next to it covering the canonical examples plus edge cases. This mirrors how LeetCode itself structures problems and lets you TDD against your solutions.

## Adding a new LeetCode problem

1. Create `leetcode/<problem_name>.py` with a `Solution` class.
2. Create `tests/test_<problem_name>.py` with the example cases from the problem.
3. `uv run pytest -k <problem_name>` while you iterate.
4. `uv run ruff format . && uv run ruff check .` before committing.

## Adding new dependencies

Runtime deps (anything `import`-ed by code that ships):

```sh
uv add numpy pandas
```

Dev-only deps (linters, test helpers, notebook tools):

```sh
uv add --dev jupyter ipykernel
```

When you're ready to expand into Pandas / ML:

```sh
uv add pandas numpy scikit-learn matplotlib
uv add --dev jupyter ipykernel        # for notebooks/
```

`uv` will resolve everything against the locked Python version and update `uv.lock`. Commit both `pyproject.toml` and `uv.lock`.

## Linting / formatting config

Ruff is configured in `pyproject.toml` under `[tool.ruff]`. The lint rule set is conservative-but-modern: pycodestyle, pyflakes, isort, bugbear, pyupgrade, flake8-simplify, and ruff's own checks. Line length is 100. Tweak `select = [...]` if you want stricter or looser.

## Why this setup

- **mise** owns interpreter/tool versions, so `mise install` reproduces the exact Python and uv across machines.
- **uv** owns dependencies, with `uv.lock` giving reproducible installs in seconds.
- **ruff** replaces black + isort + flake8 in a single, fast tool.
- **pytest** is the de-facto Python test runner; parametrised tests fit LeetCode-style example cases naturally.
- The `leetcode/` + `tests/` split keeps practice problems organised and gives you a real test-driven loop instead of pasting code into LeetCode's editor.
