# Command-Line Interface

**Category:** DX Improvement
**Quarter:** Q2-Q3
**T-shirt Size:** M

## Why This Matters

Not every chart creation task requires writing Python code. A CLI tool enables rapid prototyping from the terminal, easy integration with shell scripts and CI/CD pipelines, and accessibility for users who aren't Python developers. It transforms common operations—"publish that chart," "export all charts in a folder," "list my recent charts"—from multi-line scripts into one-liners.

A well-designed CLI also serves as living documentation of the library's capabilities.

## Current State

There is no command-line interface. All interactions require writing Python code:

```python
# Just to see your recent charts:
from datawrapper import Datawrapper
dw = Datawrapper()
charts = dw.get_my_recently_edited_charts()
for c in charts['list']:
    print(f"{c['id']}: {c['title']}")
```

The `__main__.py` file exists but only contains the `Datawrapper` class—no CLI entry point.

## Proposed Future State

A rich CLI that makes common operations trivial:

```bash
# Authentication
$ dw auth login
$ dw auth status

# Chart operations
$ dw charts list --folder marketing --limit 10
$ dw charts create bar --title "Q4 Sales" --data sales.csv
$ dw charts publish abc123
$ dw charts export abc123 --format png --output chart.png
$ dw charts delete abc123 --confirm

# Bulk operations
$ dw charts export-all --folder marketing --format pdf --output ./exports/
$ dw charts publish-all --folder marketing --dry-run

# Workspace management
$ dw workspaces list
$ dw folders list --workspace my-org
$ dw folders create "Q4 Reports" --workspace my-org

# Interactive chart builder
$ dw charts create --interactive
? Chart type: bar
? Title: Q4 Sales by Region
? Data source: sales.csv
? Primary color: #1f77b4
Creating chart... Done! https://datawrapper.dwcdn.net/abc123/

# Pipe-friendly
$ cat data.csv | dw charts create bar --title "Sales" | dw charts publish
$ dw charts list --format json | jq '.[] | .id'
```

The CLI uses `rich` for beautiful terminal output and `typer` or `click` for argument parsing.

## Key Deliverables

- [ ] **Core CLI framework** - Entry point, argument parsing, help system
- [ ] **`dw auth` commands** - Login, logout, status, token management
- [ ] **`dw charts` commands** - List, create, update, publish, export, delete
- [ ] **`dw workspaces` commands** - List, create, manage workspaces
- [ ] **`dw folders` commands** - Folder management
- [ ] **`dw batch` commands** - Bulk operations from CLI
- [ ] **Interactive mode** - Guided chart creation with prompts
- [ ] **Output formats** - Table, JSON, CSV output for scriptability
- [ ] **Progress indicators** - Rich progress bars for long operations
- [ ] **Configuration file** - `.datawrapperrc` for defaults
- [ ] **Shell completions** - Bash, Zsh, Fish completions
- [ ] **Man pages / --help** - Comprehensive documentation

## Prerequisites

- Initiative 05 (Batch Operations) - For batch CLI commands

## Risks & Open Questions

- **CLI framework choice**: `typer` (modern, type-hint-based) vs `click` (mature, widely used)?
- **Authentication storage**: Where to store tokens? Keyring? Config file? Environment only?
- **Data input**: How to handle complex data inputs? CSV paths? Stdin? Inline JSON?
- **Interactive vs scriptable**: Balance between user-friendly prompts and pipe-friendly output
- **Error messaging**: CLI errors need to be more user-friendly than Python tracebacks

## Notes

The `rich` library is already a dependency and provides:
- Beautiful tables (`rich.table.Table`)
- Progress bars (`rich.progress`)
- Syntax highlighting for JSON output
- Markdown rendering for help text

Example CLI structure using `typer`:

```python
# datawrapper/cli/__init__.py
import typer
from rich.console import Console

app = typer.Typer(help="Datawrapper CLI - Create beautiful charts from the command line")
console = Console()

@app.command()
def charts():
    """Manage charts"""
    pass

@app.command("list")
def list_charts(
    folder: str = typer.Option(None, help="Filter by folder"),
    limit: int = typer.Option(25, help="Number of charts to return"),
    format: str = typer.Option("table", help="Output format: table, json, csv")
):
    """List your charts"""
    from datawrapper import Datawrapper
    dw = Datawrapper()
    charts = dw.get_my_recently_edited_charts(limit=limit, folderId=folder)
    # Format and output...
```

Entry point in `pyproject.toml`:
```toml
[project.scripts]
dw = "datawrapper.cli:app"
```

The IPython dependency (`datawrapper/__main__.py` line 15) is used for `IFrame` display in notebooks. CLI should work without IPython installed.
