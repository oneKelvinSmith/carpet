# carpet

A Python practice monorepo. Designed to grow from LeetCode → Pandas → ML, with
each domain as its own package inside a single uv workspace.

## Toolchain

| Tool        | Purpose                                                | Pinned in               |
| ----------- | ------------------------------------------------------ | ----------------------- |
| mise        | Pins Python + uv versions                              | `mise.toml`             |
| uv          | Frontend: dependency resolution, venv, project install | `mise.toml` + `uv.lock` |
| uv_build    | Backend: turns source into installable packages        | `pyproject.toml`        |
| ruff        | Linter + formatter (replaces black, isort, flake8)     | `pyproject.toml`        |
| ty          | Type checker (Astral, beta)                            | `pyproject.toml`        |
| pytest      | Test runner                                            | `pyproject.toml`        |
| pre-commit  | Runs ruff + ty + uv-lock hooks on every commit         | `.pre-commit-config.yaml` |
| rapidfuzz   | Fuzzy-matches problem names in the scaffolder          | `pyproject.toml`        |

Python `3.13.13` and uv are pinned in `mise.toml`. When you `cd` into the repo,
mise activates them automatically (assuming mise is hooked into your shell).
`_.python.venv` in `mise.toml` also activates `.venv/`, so `python`, `pytest`,
`ruff`, `ty` etc. resolve to the project's venv without `source .venv/bin/activate`.

`UV_PYTHON_PREFERENCE = "only-system"` tells uv to use mise's Python rather than
downloading its own — one source of truth for the interpreter version.

## First-time setup

```sh
mise trust .                                # trust the mise.toml
mise install                                # install pinned Python + uv
uv sync                                     # build .venv, install carpet + all workspace members
uv run pre-commit install                   # wire up the git hook
```

## Daily workflow

```sh
uv run carpet                                  # run the repo entrypoint
uv run pytest                                  # run all tests across the workspace
uv run pytest -k two_sum                       # run a specific test
uv run ty check                                # type-check the workspace
uv run ruff check . && uv run ruff format .    # lint + format
uv run pre-commit run --all-files              # run every hook manually
```

`uv run` always executes inside the project's `.venv` — no manual activation needed.

## Project layout

```
.
├── pyproject.toml                       # workspace root + dev deps + tool config
├── uv.lock                              # locked deps across the workspace
├── mise.toml                            # pinned Python + uv versions
├── .pre-commit-config.yaml              # ruff, ty, uv-lock, hygiene hooks
├── ROADMAP.md                           # NeetCode 150 checklist
├── src/carpet/                          # repo entrypoint (uv run carpet)
│   ├── __init__.py
│   └── main.py
├── packages/                            # uv workspace members
│   └── leetcode/
│       ├── pyproject.toml
│       ├── src/leetcode/                # one module per problem
│       └── tests/                       # pytest tests for the package
└── scripts/
    └── new_problem.py                   # scaffolds a new LeetCode problem
```

`src/carpet/main.py` is the root project's CLI entrypoint, registered as
`carpet = "carpet.main:main"` in `pyproject.toml`. Run it with `uv run carpet`.

## Adding a new LeetCode problem

1. Pick a problem from `ROADMAP.md`.
2. Scaffold it:

   ```sh
   uv run python scripts/new_problem.py contains-duplicate
   # accepts slug, full LeetCode URL, partial title, or --next
   ```

   This creates `packages/leetcode/src/leetcode/<problem>.py` and
   `packages/leetcode/tests/test_<problem>.py`, looking up the title + LeetCode
   problem number from `ROADMAP.md`.
3. Implement the `Solution` class and uncomment the test parametrize block.
4. `uv run pytest -k <problem>` while iterating.
5. Tick the problem off in `ROADMAP.md`.

The scaffolder also accepts `--next` to grab the first unticked problem
automatically, or `--module` for problems whose slugs aren't valid Python names
(e.g. `3sum` → `--module three_sum`).

## Adding a new workspace member

When you're ready to start the Pandas or ML phase:

```sh
uv init --lib packages/data
```

Then in the root `pyproject.toml`:

```toml
[project]
dependencies = ["leetcode", "data"]    # ← add "data"

[tool.uv.sources]
leetcode = { workspace = true }
data = { workspace = true }            # ← add this
```

`uv sync` will install all members into the same `.venv` thereafter.

## Adding dependencies

Inside a workspace member (e.g. `packages/leetcode/`):

```sh
uv add --package leetcode <pkg>            # runtime dep for that member
```

Dev-only deps shared across the workspace, in the root:

```sh
uv add --dev <pkg>
```

Both update `uv.lock`. Commit `pyproject.toml` (the right one) and `uv.lock` together.

## Why this setup

- **mise** owns interpreter and tool versions, so `mise install` reproduces the
  exact Python and uv across machines.
- **uv + uv_build** owns dependencies, project installs, and packaging — one
  toolchain for the full lifecycle.
- **ruff** replaces black + isort + flake8 + pyupgrade in a single, fast binary.
- **ty** type-checks the workspace; Astral toolchain alignment.
- **pre-commit** runs ruff, ty, and `uv lock --check` on every commit so the
  repo stays consistent.
- **uv workspaces** let each practice domain (leetcode, eventually data + ml)
  be its own installable package while sharing one venv, one lockfile, one
  set of dev deps.
- **pytest parametrize** fits LeetCode-style example cases naturally; no
  need to manually write each variant.
