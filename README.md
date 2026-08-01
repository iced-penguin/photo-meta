# photo-meta

A small Python CLI for writing description metadata to image files via exiftool.

## Requirements

- Python 3.12+
- exiftool

## Usage

Write metadata with the `meta` subcommand:

```bash
uv run python main.py meta --config photo-meta.toml "img*.jpg"
```

You can also override the config value from the command line:

```bash
uv run python main.py meta --description "Great photo." "img*.jpg"
```

## Local install

```bash
pip install -e .
```

## Test

Run the test suite with:

```bash
pytest
```

If you are using uv, you can also run:

```bash
uv run pytest
```