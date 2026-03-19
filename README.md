# SnipVault

A simple command-line snippet manager. Save, retrieve, search, and organize code snippets by name and tag — all from your terminal.

## Why this project?

An experimentation project to explore Claude Code while building a Python CLI from scratch.

## Quick Start

```bash
git clone <repo-url>
cd snipvault
pip install -e .
```

The vault is stored at `~/.snipvault/vault.json` and created automatically on first use.

## Usage

```bash
# Add a snippet (tags are optional)
snipvault add <name> "<snippet>" --tags <tag1> <tag2>

# Retrieve a snippet
snipvault get <name>

# List all snippets
snipvault list

# Search by name, content, or tag
snipvault search <query>

# Delete a snippet
snipvault delete <name>
```

### Examples

```bash
snipvault add hello "print('hello, world')" --tags python basics
snipvault add curl-json "curl -s -H 'Content-Type: application/json'" --tags bash curl

snipvault get hello
snipvault search bash
snipvault list
snipvault delete hello
```

## Testing

```bash
pip install pytest
python -m pytest -v
```
