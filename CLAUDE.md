# SnipVault – Claude Code Guidelines

## Workflow

- Create a new branch for each feature or fix before making changes
- Run tests before committing: `python -m pytest -v`
- Keep commits focused — one logical change per commit

## Code Style

- Follow existing patterns in the codebase before introducing new ones
- Keep functions small and single-purpose
- No external dependencies unless clearly necessary — add them to `pyproject.toml`

## Testing

- All new features must include tests in `tests/test_vault.py`
- Use the `tmp_vault` fixture (a `tmp_path`-based vault) to avoid touching the real vault
- Test the vault logic directly, not through the CLI

## Project Structure

- `storage.py` — persistence only, no business logic
- `vault.py` — business logic, no I/O beyond delegating to storage
- `cli.py` — user interaction only, delegates everything to vault functions
