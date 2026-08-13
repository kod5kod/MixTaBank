# AGENTS.md

> Primary instruction file for all coding agents (globally).

---

## Project: MixTaBank

MixTaBank is a curated collection of heterogeneous mixed-type tabular datasets tailored for evaluating tabular generative models under realistic, human-centric conditions. Designed for both academic researchers and professional practitioners, this repository provides optimized, ready-to-use tabular data from Kaggle and UCI.

**Primary goals:**

1. **Curated Datasets** — Provide a curated set of real-world datasets varying in size, complexity, heterogeneity, and cardinality.
2. **Polars-Native Efficiency** — The library's core internals are strictly built on Polars to maximize speed and memory efficiency (with a `to_pandas()` option for user convenience).
3. **Curated Recipes** — Implement dataset-specific preprocessing recipes directly imported from the dataset metadata files (`.md`) to enable reproducible preprocessing without complex encoding logic.
4. **Mass Download CLI/API** — Ensure users can batch-download and process multiple tabular datasets quickly for large-scale benchmarks.

---

## Environment

| Setting             | Value         |
|---------------------|---------------|
| Python version      | >= 3.13       |
| Environment manager | uv            |
| Environment name    | .venv         |

**Always activate the environment before running commands:**

```bash
source .venv/bin/activate && <command>
# or for windows:
.\.venv\Scripts\activate && <command>
```

Never use a globally installed Python. Always use the project environment (`uv run` is also acceptable).

---

## Project Structure

```
MixTaBank/
│
├── .github/                        # CI workflows
├── docs/                           # Method documentation and design plans
│   ├── overhaul_plan.md            # Master framework overhaul plan
│   └── datasets/                   # Dataset-specific markdown info files & curated recipes
│
├── configs/                        # All execution configs (.toml)
│   └── config.toml                 # Primary config (paths, seeds, defaults)
│
├── mixtabank/                      # Installable library code
│   ├── __init__.py
│   ├── data_src_dict/              # Dataset metadata lookup maps (JSON/YAML)
│   └── src/
│       ├── utils.py                # Legacy utils (to be modularized)
│       ├── loaders.py              # Polars-native dataset loaders
│       ├── splits.py               # Deterministic, stratified split logic
│       └── metadata.py             # DataFrame inspection and metadata summary
│
├── download_dataset.py             # CLI command entry point for mass downloads
│
├── tests/                          # Pytest suite
│   ├── conftest.py
│   ├── test_loaders.py
│   └── test_splits.py
│
├── pyproject.toml                  # Standard package configuration
├── requirements.txt                # Runtime dependencies
├── LICENSE
└── README.md
```

---

## Development Commands

```bash
# Run all tests
uv run pytest

# Lint (check only)
uv run ruff check mixtabank/ tests/

# Format
uv run ruff format mixtabank/ tests/
```

---

## Dependency Management

- **Runtime dependencies:** `pyproject.toml` `[project.dependencies]` (locked in `uv.lock`).
- **Dev dependencies:** `pyproject.toml` `[dependency-groups.dev]`.
- **Polars-Only Rule:** The library internals are strictly Polars-only. Do not use Pandas in the core API files (`loaders.py`, `splits.py`, `metadata.py`). If the user explicitly asks to receive Pandas, call `.to_pandas()` strictly at the API boundaries.
- **Never** add or remove dependencies without asking the user first.
- Prefer minimal, well-maintained packages; flag transitive bloat when encountered.

---

## Code Standards

- **Type hints:** Required on all new functions and methods.
- **Docstrings:** NumPy-style docstring format.
- **Style:** PEP 8, enforced by `ruff`.
- **Functions:** Small and single-purpose.
- **No duplication:** Extract shared logic into helpers.
- **No inheritance by default:** Prefer composition.
- **Dataclasses:** Prefer returning structured `dataclass` objects over raw tuples when returning dataset payloads.
- **Comments:** Write comments when the WHY is non-obvious — hidden constraints, subtle invariants, workarounds, or non-standard algorithmic choices. Do not narrate what the code does; well-named identifiers already do that.
- **Error handling:** Do not add error handling for scenarios that cannot happen. Validate only at system boundaries (e.g., user input, Kaggle/UCI network calls). Handle API rate limits gracefully.
- **Imports:** Absolute imports preferred; ordering stdlib → third-party → local.
- **Print vs logging:** Use the `logging` module in library code (`mixtabank/`). `print()` is acceptable in scripts (`download_dataset.py`) or standalone demos.
- **Tests:** You must add unit tests for each new feature you implement. Make sure to add all required tests and verify they pass with `pytest`.

---

## Configuration & Environment Variables

- **Config location:** `configs/`
- Use `.toml` files for configuration.
- Machine-specific **roots** come from the environment, not the config. Set them in an untracked `.env` file (use `.env.example` as a template).
- Never hardcode environment-specific values (paths, credentials) in source files **or in committed configs** — use a placeholder and document it in `.env.example`.

---

## Testing

- **Framework:** pytest
- **Run with:** `pytest`
- All new features and bug fixes require tests.
- Tests live in `tests/` and mirror the library structure.
- Shared fixtures go in `tests/conftest.py`.

---

## Agent Autonomy

### Allowed without asking:
- Reading any file in the repository.
- Running tests, linting, formatting, type checks.
- Editing or creating files **when part of a clearly stated task**.

### Must ask before:
- Any `git` operation: `commit`, `push`, `merge`, `rebase`, `reset`.
- Deleting files or directories.
- Installing, upgrading, or removing dependencies.
- Modifying configuration files (`requirements.txt`, CI configs).
- Any change **outside the stated task scope** (e.g., unsolicited refactors, style fixes on untouched files).
- Any action with effects outside this repository.
- Continuing a task that spans more than ~5 files without pausing — break large work into logical chunks, report after each, and confirm before proceeding.

### When uncertain:
Stop and ask. Do not guess at scope, approach, or intent.
If you encounter the same error 3 times while trying to fix a test or run a command, stop and ask the user for help.

### When a task is complete, always report:
1. All files created or modified, with a one-line description of each change.
2. Test and lint results.
3. Any follow-up items, open questions, or known limitations.

---

## Documentation & Artifacts

- **Implementation plans:** Before complex refactors or multi-file features, write a brief plan and get approval before writing any code. Always save agent plans in the `docs/` directory (e.g. `overhaul_plan.md`).
- **Dataset Recipes:** Dataset info files in `docs/datasets/` should cleanly document any specific preprocessing logic ("curated recipes") applied.
- **Changelog Updates:** Always update `CHANGELOG.md` to reflect any new releases, features, or significant bug fixes.

---

## Security

- Never commit secrets, API keys, Kaggle tokens, or `.env` file contents.
- Validate all inputs at system boundaries.
