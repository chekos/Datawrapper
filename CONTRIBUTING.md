# How to contribute

## Dependencies

Clone the repository. Move into the directory on your terminal.

Install dependencies for development.

```sh
uv sync
```

Install pre-commit to run a battery of automatic quick fixes against your work.

```sh
uv run pre-commit install
```

### Tests

You can run unit tests to verify the library is working with the following:

```bash
uv run pytest --cov -sv
```

We also enforce ruff for linting, handled primarily via pre-commit. You can run it manually like so:

```bash
uv run ruff check ./datawrapper
```

We also enforce static typing with mypy, also handled via pre-commit. You can run it manually like so:

```bash
uv run mypy ./datawrapper --ignore-missing-imports
```

### Before submitting

Before submitting your code please do the following steps:

1. Add any changes you want
1. Add tests for the new changes
1. Run tests
1. Run the pre-commit hooks
1. Edit documentation if you have changed something significant

Now you're ready to submit your pull request.
