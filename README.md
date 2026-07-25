# photo-cli

A small Python CLI for writing description metadata to image files via exiftool.

## Requirements

- Python 3.12+
- exiftool

## Usage

```bash
uv run python main.py "path/to/*.jpg"
```

You can also pass explicit files:

```bash
uv run python main.py "img1.jpg" "img2.jpg"
```
