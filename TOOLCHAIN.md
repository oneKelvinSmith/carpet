# The carpet toolchain, layer by layer

A guided tour of every tool, file, and convention that makes this repo work — written to be read once front-to-back, then referenced when something breaks.

## How to use this doc

- **First read**: top to bottom. Each layer builds on the previous one; skipping ahead will leave gaps.
- **Later**: jump to a section via the table of contents when you hit a specific problem.
- Every section ends with **Verify on your machine** — concrete commands to confirm you've internalised it, not just read it.

## Prerequisites

You should already know:

- The difference between an *interpreter* (`python`) and a *package manager* (`pip`/`uv`).
- That `pyproject.toml` is the modern replacement for `setup.py` + `setup.cfg`.

You do **not** need prior experience with `mise`, `uv`, `ruff`, or `ty` — those are what this doc teaches. The next section covers virtual environments from scratch, since the rest of the doc assumes you understand them.

## Background: Python virtual environments

Every layer below this one ends up touching the venv, so we need to nail down what one actually is before going further.

### The problem venvs solve

You have one Python installed on your machine. Project A needs `requests==2.28`. Project B needs `requests==2.31`. Without isolation, installing one breaks the other — there's a single `site-packages/` directory shared across everything.

A **virtual environment** (venv) is just a folder on disk that gives a single project its own `site-packages/`. Each project gets its own isolated set of installed libraries; the system Python stays untouched.

### What a venv actually is

It's a directory. Nothing magic. In carpet, it's `.venv/` at the repo root. Look inside:

```sh
ls .venv/
# bin/  lib/  pyvenv.cfg
```

The pieces:

- **`bin/python`** — a *symlink* to the real Python interpreter (in our case, mise's CPython at `~/.local/share/mise/installs/python/3.13.13/bin/python3`). A venv does **not** copy Python; it just creates a pointer.
- **`bin/pytest`, `bin/ruff`, `bin/new-problem`** — small scripts ("shims") with a shebang that points at `.venv/bin/python`. When you run them, the shebang routes them through the venv's Python.
- **`lib/python3.13/site-packages/`** — where installed libraries live. This is the actual isolation: `pip install foo` (or `uv sync`) drops files here, **not** in the system Python's site-packages.
- **`pyvenv.cfg`** — metadata file telling Python "this is a venv, the real interpreter is over there."

### How Python finds the venv

When you run `.venv/bin/python`, Python checks `pyvenv.cfg`, sees it's in a venv, and prepends `.venv/lib/python3.13/site-packages/` to `sys.path` ahead of the system site-packages. Imports find venv-installed libraries first.

When you run a script with `#!/path/to/.venv/bin/python3` as its shebang, the same thing happens — that's why `.venv/bin/pytest` "knows" to use the venv's libraries.

### Activation (and why this repo doesn't need it manually)

Traditionally you'd "activate" a venv with `source .venv/bin/activate`, which prepends `.venv/bin/` to your shell's `PATH`. After that, typing `python` resolves to `.venv/bin/python` instead of the system one.

In carpet, **mise activates the venv automatically** when you `cd` into the repo, via `_.python.venv = ".venv"` in `mise.toml` (covered in Layer 1). So `pytest` at the prompt just works — no manual `source` step.

And `uv run <cmd>` ignores activation entirely: it executes `<cmd>` inside the venv directly, regardless of whether your shell has it activated.

### Why this matters for the rest of the doc

- **Layer 1 (mise)** installs the *real* Python that the venv symlinks to.
- **Layer 2 (uv)** creates the venv (`uv sync` does this automatically) and installs deps into it.
- **Layer 3** is the interpreter as seen *through* the venv's symlink.
- **Layer 5 (packages)** installs your own code into the venv's `site-packages/` just like third-party libraries.
- **Layer 7 (tests)** runs pytest from `.venv/bin/pytest`, which uses the venv's interpreter and finds your packages in the venv's `site-packages/`.

### Verify on your machine

```sh
ls .venv                                 # bin/  lib/  pyvenv.cfg
cat .venv/pyvenv.cfg                     # metadata pointing at mise's Python
readlink .venv/bin/python                # symlink target — the "real" interpreter
ls .venv/lib/python3.13/site-packages/   # every installed library, one dir each
.venv/bin/python -c "import sys; print(sys.path)"   # venv's path first
```

That last command is the most illuminating: it prints the import-search path. The venv's `site-packages/` appears before any system path, which is the entire mechanism of isolation.

## The mental model

Think of the toolchain as a pipeline. Each layer's job is to make the next layer's job possible:

```
mise          → pins which Python and which uv exist on disk
  ↓
uv            → uses those, builds a venv, installs deps from the lockfile
  ↓
Python        → the interpreter inside the venv
  ↓
libs + tools  → what's installed alongside Python
  ↓
packages      → your own code, treated as installed libraries
  ↓
build         → how source code becomes installable
  ↓
tests         → how you verify the whole thing works
  ↓
runtime       → what actually executes when you type a command
```

Every layer is **declarative and reproducible**. A fresh clone on a new machine reproduces the same state by re-running each layer top-to-bottom.

## Table of contents

1. [mise — version manager for tools](#1-mise--version-manager-for-tools)
2. [uv — resolver, installer, runner](#2-uv--resolver-installer-runner)
3. [Python — the interpreter](#3-python--the-interpreter)
4. [Libraries and tools — the dependency surface](#4-libraries-and-tools--the-dependency-surface)
5. [Packages — workspace members](#5-packages--workspace-members)
6. [Build — turning source into installable packages](#6-build--turning-source-into-installable-packages)
7. [Tests — framework and philosophy](#7-tests--framework-and-philosophy)
8. [Runtime — what happens when you type `uv run pytest`](#8-runtime--what-happens-when-you-type-uv-run-pytest)
9. [Debugging the toolchain](#9-debugging-the-toolchain)
10. [Glossary](#10-glossary)
11. [Further reading](#11-further-reading)

---

## 1. mise — version manager for tools

### The model

`mise` pins the *interpreter* and the *package manager* themselves, before anything project-specific runs. Without mise, you'd have to manually install the right Python and uv before you could even start.

Think of mise as one layer below "language tooling": it manages the tools that manage your project.

### Where it lives

`mise.toml` at the repo root.

```toml
[tools]
python = "3.13.13"
uv = "<pinned version>"

[env]
_.python.venv = ".venv"
UV_PYTHON_PREFERENCE = "only-system"
```

### What each piece does

- **`[tools] python = "3.13.13"`** — `mise install` downloads CPython 3.13.13 and stores it at `~/.local/share/mise/installs/python/3.13.13/`. The venv's `python` symlink will point there.
- **`[tools] uv = "..."`** — same idea for uv. Pinning uv with mise means the *resolver* version is reproducible, not just the interpreter.
- **`_.python.venv = ".venv"`** — when you `cd` into the repo, mise activates `./.venv`, so `python`, `pytest`, `ruff` resolve to the venv's binaries without `source .venv/bin/activate`. This is why typing `pytest` in the project shell just works.
- **`UV_PYTHON_PREFERENCE = "only-system"`** — tells uv "don't go download your own Python; use whatever the system (mise) gives you." Without this, uv would happily fetch a separate CPython, leaving two interpreters with no canonical choice.

### Why mise at all?

The alternative is `pyenv` (for Python versions) + `pipx install uv` (for uv) + remembering to keep both updated. mise unifies these into one declarative file. New machine = `mise install` and you have an identical setup. No "works on my machine because I have uv 0.4 and you have 0.7."

### Why mise manages Python here, not uv

uv has its own Python-installation feature (`uv python install 3.13`) and can pin a version via `.python-version` or via `requires-python` in `pyproject.toml`. We could let uv own Python and drop it from `mise.toml`. We don't, for four reasons:

1. **mise is already in the stack.** It owns env vars and tasks. Letting it also pin Python adds zero new tools.
2. **One source of truth for "what does this project need to run."** `mise.toml` is the file you point a new contributor at. Splitting Python's version across `mise.toml` *and* a uv-owned `.python-version` would dilute that authority for no functional gain.
3. **Polyglot future-proofing.** If you later add Node, Rust, or Go (e.g. a visualisation frontend or a perf demo), mise extends naturally — `[tools] node = "20"`. uv only handles Python.
4. **The handshake is explicit.** `UV_PYTHON_PREFERENCE = "only-system"` (set in `mise.toml`) is the one-line contract that says "mise owns Python, uv defers to whatever mise provides." Self-documenting, no surprises.

The reverse choice would be right if carpet had to run in a context where mise can't be installed (e.g. constrained CI runners, minimal Docker images, servers that just `pip install uv && uv sync`), or if leetcode were a published PyPI package whose users shouldn't need mise. Neither applies to a personal practice monorepo.

The clean separation of concerns to remember:

```
mise:  versions of tools (python, uv, future Node/Go), env vars, tasks
uv:    dep resolution, lockfile, venv contents, installs
```

### Verify on your machine

```sh
mise current               # shows python + uv versions currently active
which python               # should point inside ~/.local/share/mise/installs/...
which uv                   # should also be a mise shim
echo $UV_PYTHON_PREFERENCE # should print: only-system
```

If `which python` points at `/usr/bin/python3` or homebrew, mise isn't hooked into your shell. Check `~/.zshrc` for `mise activate zsh`.

---

## 2. uv — resolver, installer, runner

### The model

`uv` owns everything between "I have a Python interpreter" and "I have a working environment." Resolution, locking, installing, venv creation, running commands. It's the modern unified frontend that replaces `pip` + `pip-tools` + `virtualenv` + `pipenv` + `poetry`.

### Where it lives

- Root `pyproject.toml` for project config (sections starting with `[project]`, `[tool.uv...]`).
- `uv.lock` for resolved dep versions — committed to git.

### The three subcommands to know

#### `uv sync`

Reads `pyproject.toml` + `uv.lock`, builds `.venv/`, installs the workspace + every dependency. Idempotent — running it twice in a row does nothing the second time. This is the "make my environment match the lockfile" command.

#### `uv lock`

Solves the dependency graph and writes `uv.lock` — exact versions, hashes, source URLs. Committed to git so every checkout resolves identically.

> **The pre-commit hook**: `.pre-commit-config.yaml` runs `uv-lock` on every commit. This guards against `pyproject.toml` drifting out of sync with `uv.lock` — if you edit deps without re-locking, the hook re-locks and stages the updated file.

#### `uv run <cmd>`

Two things in one: (a) make sure the venv is up to date with the lockfile, then (b) execute `<cmd>` inside it. Roughly equivalent to `source .venv/bin/activate && <cmd>`, but with an automatic sync step. A fresh clone can just `uv run pytest` without explicit `uv sync` first.

### Workspaces

Carpet is a **monorepo** via uv's workspace feature:

```toml
# root pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]

[tool.uv.sources]
leetcode = { workspace = true }
```

Every `packages/*/pyproject.toml` is a workspace member. They share *one* venv, *one* `uv.lock`, and *one* set of dev deps. `{ workspace = true }` tells the root `carpet` package "when I depend on `leetcode`, use the in-tree version, not PyPI."

This is the magic that lets you add new domains (e.g. `packages/data/`) and have them automatically pick up dev tools and share the venv with `packages/leetcode/`.

### Verify on your machine

```sh
uv --version                # confirm uv is on PATH
uv sync                     # should print "Resolved N packages in Xms"
ls .venv/bin                # should show python, pytest, ruff, ty, carpet, new-problem
uv run python -c "import leetcode; print(leetcode.__file__)"
# should print: .../packages/leetcode/src/leetcode/__init__.py
```

The last command verifies the workspace member is installed *in editable mode* — `import leetcode` resolves to the in-tree source, so edits are reflected without reinstalling.

---

## 3. Python — the interpreter

### The model

This is the layer most people think about, but in our pipeline it's almost a passive participant: mise installs it, uv plugs it into a venv, everything else uses what's in the venv.

### Path chain

```
mise installs:  ~/.local/share/mise/installs/python/3.13.13/bin/python3
venv symlink:   .venv/bin/python → that interpreter
shebangs:       .venv/bin/pytest #!/Users/<you>/Code/carpet/.venv/bin/python3
```

A venv is **not** a copy of Python — it's a directory with symlinks to the underlying interpreter plus its own `site-packages/`.

### The `requires-python` claim

```toml
# root pyproject.toml
[project]
requires-python = ">=3.13"
```

This is the *project's* claim about what it needs. uv enforces it during resolution — if mise gave you 3.12, `uv sync` would fail with a clear error.

### Why this layer matters: the directory rename trap

Shebangs in `.venv/bin/*` are **absolute paths**. If you rename or move the project directory, every shebang still points at the old path:

```sh
cat .venv/bin/pytest
#!/Users/<you>/Code/play/.venv/bin/python3   # ← old path
```

Symptom: `uv run pytest` fails with `Failed to spawn: pytest. Caused by: No such file or directory (os error 2)` — confusing because `pytest` clearly exists.

Fix: `uv venv --clear && uv sync` rebuilds the venv with correct shebangs.

> This is what happened in this repo after renaming `play → carpet`. The `new-problem` script worked because it had just been regenerated; pytest was untouched and kept the stale shebang.

### Verify on your machine

```sh
.venv/bin/python --version              # should say 3.13.13
readlink .venv/bin/python               # should resolve to mise's CPython
head -1 .venv/bin/pytest                # shebang should reference current project path
```

---

## 4. Libraries and tools — the dependency surface

### The model

Two distinct dependency groups, with different lifecycles:

- **Runtime deps**: what the package needs to function. Ships with the wheel.
- **Dev deps**: what *developers* need to work on the package. Never ships.

### Where they live

```toml
# root pyproject.toml
[project]
dependencies = ["leetcode"]              # runtime — what carpet needs to run

[dependency-groups]
dev = ["pre-commit>=4.0", "pytest>=8.3", "rapidfuzz>=3.10", "ruff>=0.8", "ty>=0.0.37"]
```

The `[dependency-groups]` syntax is **PEP 735** — the modern replacement for `[tool.poetry.dev-dependencies]` or `requirements-dev.txt`. `uv sync` installs the default group (`dev`) automatically; you can opt out with `--no-dev`.

### Each tool's role

| Tool | Job | Replaces |
|---|---|---|
| `pre-commit` | Run hooks on `git commit` | — |
| `pytest` | Test runner, assertion rewriter, fixtures | `unittest` |
| `rapidfuzz` | Fast fuzzy string matching (used by `_scaffold.py` for partial title lookup) | `fuzzywuzzy` |
| `ruff` | Linter + formatter, written in Rust | `black` + `isort` + `flake8` + `pyupgrade` |
| `ty` | Type checker (Astral, beta) | `mypy` |

### The all-Astral angle

`uv` + `ruff` + `ty` are all built by Astral. Shared toolchain means:
- Compatible release cadences — version-bumping one rarely breaks the others.
- Consistent config conventions across `[tool.ruff]`, `[tool.uv]`, etc.
- Cross-cutting features (e.g. ruff respecting uv's workspace boundaries) tend to land coherently.

### Config consolidation

All tool config lives in `[tool.<name>]` tables in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "RUF"]

[tool.ty.src]
include = ["src", "packages"]

[tool.pytest.ini_options]
testpaths = ["packages"]
```

No `.flake8`, `.isort.cfg`, `mypy.ini` litter. One file owns project metadata *and* tool config.

### Verify on your machine

```sh
uv run ruff check .                     # lint pass
uv run ruff format --check .            # format check (no changes)
uv run ty check                         # type check
uv run pre-commit run --all-files       # run every hook on every file
```

---

## 5. Packages — workspace members

### The model

A workspace member is a directory with its own `pyproject.toml`, installable as a real Python package, but sharing the workspace's venv and lockfile.

### Layout

```
packages/leetcode/
├── pyproject.toml          # package metadata
├── ROADMAP.md              # package-owned docs
├── src/leetcode/           # importable code (src layout)
│   ├── __init__.py
│   ├── _scaffold.py        # new-problem CLI
│   ├── two_sum.py          # one module per problem
│   └── ...
└── tests/                  # tests live outside src/
```

### The src layout

Source code under `src/<pkgname>/`, not directly at the package root.

**Why?** Without src layout, `import leetcode` could resolve to the *checked-out source directory* rather than the *installed package*. That sounds convenient but it masks problems:

- Missing dependencies that the install would have caught.
- Packaging mistakes (forgetting to include a subpackage in the wheel).
- Tests that pass locally but fail after install.

With src layout, `import leetcode` only works if leetcode is **actually installed** in the venv. The test environment matches the published environment.

### Console scripts

```toml
# packages/leetcode/pyproject.toml
[project.scripts]
new-problem = "leetcode._scaffold:main"
```

At install time, the build backend reads `[project.scripts]` and generates `.venv/bin/new-problem` — a small Python shim that imports `leetcode._scaffold` and calls `main()`.

> **Why `_scaffold.py` and not `new_problem.py`?** The package directory will fill with problem modules (`two_sum.py`, `valid_anagram.py`, ...). A file named `new_problem.py` would visually look like just another problem. The leading underscore signals "tooling, not a problem" without affecting the console script name.

### The path-resolution pattern

A console script doesn't know where it's invoked from. `_scaffold.py` uses this trick:

```python
# .../packages/leetcode/src/leetcode/_scaffold.py → .../packages/leetcode
PACKAGE_ROOT = Path(__file__).resolve().parents[3]
```

`__file__` is the script's location; `parents[3]` walks up four levels to the package root. Everything else (`SRC_DIR`, `TESTS_DIR`, `ROADMAP_PATH`) is computed relative to that. Result: `uv run new-problem` works from any directory.

### Verify on your machine

```sh
ls .venv/bin/new-problem               # exists after uv sync
cat .venv/bin/new-problem              # tiny shim importing leetcode._scaffold
uv run new-problem --help              # entry point works
cd /tmp && uv run --project ~/Code/carpet new-problem --help
# still works — script knows its own paths
```

---

## 6. Build — turning source into installable packages

### The model

When uv installs a package, it doesn't just copy files — it goes through the standard Python **build backend** protocol (PEP 517) to produce a wheel, then installs the wheel.

### Configuration

```toml
# packages/leetcode/pyproject.toml
[build-system]
requires = ["uv_build>=0.11,<0.12"]
build-backend = "uv_build"
```

### The flow

When `uv sync` installs `leetcode`:

1. Reads `[build-system]` — "use `uv_build` as the build backend."
2. Spawns an **isolated build environment**, installs `uv_build` there.
3. Calls `uv_build`'s PEP 517 hooks (`build_wheel`, `build_sdist`).
4. `uv_build` sees the src layout, finds `src/leetcode/`, packages it into a wheel.
5. Wheel gets installed into `.venv/lib/python3.13/site-packages/leetcode/`.
6. `[project.scripts]` entries become executables in `.venv/bin/`.

This is the modern Python packaging contract (PEPs 517, 518, 621, 660).

### Why isolated build env?

So that the build process can't accidentally depend on whatever happens to be in your dev venv. If `uv_build` needs `tomli`, it installs `tomli` in the build env — your project doesn't have to declare it.

### Other backends you could use

`uv_build` is one option among many. Common alternatives:

- `setuptools` — the historical default, still widely used.
- `hatchling` — popular, fast, similar to `uv_build`.
- `flit_core` — minimal, for pure-Python projects.
- `poetry-core` — if you use Poetry for everything.

We use `uv_build` because it's by Astral (same vendor as uv), optimised for use with uv, and Just Works™ for src-layout pure-Python packages.

### Verify on your machine

```sh
uv build --package leetcode             # builds wheel + sdist in dist/
ls dist/                                # see leetcode-0.1.0-py3-none-any.whl
unzip -l dist/leetcode-0.1.0-*.whl      # peek inside — should contain src layout
```

---

## 7. Tests — framework and philosophy

### Configuration

```toml
# root pyproject.toml
[tool.pytest.ini_options]
minversion = "8.0"
addopts = ["-ra", "--strict-markers", "--strict-config", "--import-mode=importlib"]
testpaths = ["packages"]
```

### Each addopt explained

- **`-ra`** — show extra summary info for everything except passing tests (skipped, expected fail, errors). Default summary is too quiet.
- **`--strict-markers`** — `@pytest.mark.foo` errors unless `foo` is registered. Catches typos in marker names.
- **`--strict-config`** — error on unknown config keys. Catches typos in this very block.
- **`--import-mode=importlib`** — the modern, recommended import mode. Tests are imported via `importlib` directly rather than the legacy `sys.path`-mangling approach. Required for:
  - src layout (no need for `__init__.py` in `tests/`).
  - Multiple packages with `tests/conftest.py` files (no module-name collisions).
  - Modern type-checker compatibility.
- **`testpaths = ["packages"]`** — start collection here, walk down, find `test_*.py`. pytest recursively walks every subdirectory under this.

### Why `testpaths = ["packages"]` and not `["packages/*/tests"]`?

The broader path doesn't require every workspace member to use `tests/`. Cost: pytest walks non-test dirs (`src/`, `__pycache__/`) too, but at this scale it's invisible. Benefit: zero coupling between pytest config and project layout convention.

If you ever start writing `*_test.py` files inside `src/` (e.g. for inline doctests) and pytest accidentally collects them, *then* tighten to `packages/*/tests`.

### Philosophy: parametrize over duplication

Look at any test file:

```python
@pytest.fixture
def solution() -> Solution:
    return Solution()

@pytest.mark.parametrize(
    ("nums1", "m", "nums2", "n", "expected"),
    [
        ([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, [1, 2, 2, 3, 5, 6]),
        ([1], 1, [], 0, [1]),
    ],
)
def test_merge_sorted_array(solution, nums1, m, nums2, n, expected):
    solution.merge(nums1, m, nums2, n)
    assert nums1 == expected
```

The shape — one fixture per Solution, one parametrize block per method — maps directly onto LeetCode's "here's the function, here are example cases" format. Each row becomes an independent test node with its own pass/fail line. You get coverage breadth without writing 12 `def test_case_n():` functions.

The `_scaffold.py` test template bakes this shape in for every new problem, so you start with the right pattern automatically.

### Verify on your machine

```sh
uv run pytest                              # run everything
uv run pytest -v                           # verbose, see each parametrize row
uv run pytest -k two_sum                   # filter by keyword
uv run pytest --collect-only               # see what would run without running
uv run pytest packages/leetcode/tests/test_two_sum.py::test_two_sum
                                           # one specific test
```

---

## 8. Runtime — what happens when you type `uv run pytest`

End-to-end trace, ground truth for "where does my keystroke go":

1. **Shell PATH resolves `uv`** — mise prepends `~/.local/share/mise/shims/` to PATH, so `uv` is a mise shim that delegates to the mise-pinned binary.
2. **uv reads `pyproject.toml` + `uv.lock`** — figures out what should be in the venv.
3. **uv reconciles the venv** — installs/removes anything out of date. Most invocations are no-ops here.
4. **uv invokes `.venv/bin/pytest`** — the shim has a shebang pointing at `.venv/bin/python3` → mise-managed CPython 3.13.13.
5. **pytest starts** — reads `[tool.pytest.ini_options]`, applies addopts, registers conftest fixtures.
6. **Collection phase** — pytest walks `testpaths = ["packages"]`, finds `test_*.py` files, imports each via `importlib`. Imports like `from leetcode.two_sum import Solution` resolve via the *installed* package in `.venv/lib/python3.13/site-packages/leetcode/` (the src-layout payoff).
7. **Execution phase** — each test node (each parametrize row) runs as its own item; the `solution` fixture builds a fresh `Solution()` for each.
8. **Reporting phase** — pytest prints results, `-ra` shows the summary, exit code 0 or non-zero.

Every layer above is pinned, so this whole pipeline reproduces from a fresh `git clone`.

---

## 9. Debugging the toolchain

### Where to look when things break

| Symptom | Probable layer | First check |
|---|---|---|
| `command not found: uv` | mise | `mise current` shows uv? Shell has `mise activate`? |
| `mise: tool not installed: python@3.13.13` | mise | `mise install` |
| `error: The Python request '>=3.13' could not be satisfied` | uv ↔ mise | mise has matching Python? `mise current` |
| `Failed to spawn: pytest. No such file or directory` | Python | Stale venv shebangs. `uv venv --clear && uv sync` |
| `ModuleNotFoundError: No module named 'leetcode'` | packages | Did you `uv sync` after adding the workspace member? |
| `ImportError: attempted relative import` in tests | tests | `--import-mode=importlib` missing from `pyproject.toml`? |
| `pytest discovers 0 tests` | tests | `testpaths` correct? Files named `test_*.py`? |
| Pre-commit fails on `uv-lock` | uv | Edit to `pyproject.toml` deps without re-locking. Run `uv lock` and re-commit. |
| `ruff check` complains about a rule you didn't write | libs+tools | Check `[tool.ruff.lint] select` — `B`, `UP`, `SIM` etc. each enable a family of rules. |

### General principle

Each layer is **inspectable on disk**:

- mise's state: `~/.local/share/mise/`
- uv's state: `.venv/`, `uv.lock`
- Python's state: `.venv/lib/python3.13/site-packages/`
- Pytest's state: `pyproject.toml` `[tool.pytest.ini_options]`

When confused, drop into one layer and use the **Verify on your machine** commands from that section.

---

## 10. Glossary

- **Backend (build)** — the library that turns `pyproject.toml` + source code into a wheel. Called via PEP 517 hooks.
- **Editable install** — installing a package such that `import` resolves to the source directory; edits don't require reinstall. `uv sync` does editable installs of workspace members.
- **Entry point / console script** — a shell command (e.g. `new-problem`) that, when run, imports a Python function and calls it.
- **Frontend (package manager)** — what the user invokes to install/resolve (uv, pip, poetry). Talks to the backend via PEP 517.
- **Lockfile** — exact pinned versions of every dep, transitively. `uv.lock` here.
- **PEP 517 / 518 / 621 / 735** — Python Enhancement Proposals defining build backend protocol, build-system table, project metadata table, dependency groups respectively.
- **Shim** — small executable that delegates to another. mise uses shims to route `python`/`uv` through its version manager.
- **Src layout** — packaging convention where source lives in `src/<pkg>/` so `import <pkg>` only resolves to the installed package.
- **Wheel** — Python's binary distribution format (`*.whl`). A zip file with a specific layout that pip/uv can install without running setup code.
- **Workspace** — a uv concept: multiple packages in one repo sharing a venv and lockfile.

---

## 11. Further reading

Skim the official docs once you're comfortable with this doc:

- **uv**: https://docs.astral.sh/uv/ — workspaces, scripts, settings reference.
- **uv workspaces specifically**: https://docs.astral.sh/uv/concepts/projects/workspaces/
- **mise**: https://mise.jdx.dev/ — config, shell integration, version-pinning conventions.
- **ruff**: https://docs.astral.sh/ruff/ — rule reference, config reference.
- **ty**: https://github.com/astral-sh/ty — early-stage but worth tracking.
- **pytest**: https://docs.pytest.org/ — fixture model, parametrize, marker reference. The "How-to" section is more useful than the tutorial.
- **PEP 517** (build system spec): https://peps.python.org/pep-0517/
- **PEP 621** (project metadata in `pyproject.toml`): https://peps.python.org/pep-0621/
- **PEP 735** (dependency groups): https://peps.python.org/pep-0735/

When you start adding the next workspace member (`packages/data/`, eventually `packages/ml/`), re-read sections 5 and 6 — they're the layers most affected by adding a member.
