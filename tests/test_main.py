import sys
from pathlib import Path

import main


def test_meta_reads_description_from_config(tmp_path, monkeypatch):
    config_file = tmp_path / "photo-cli.toml"
    config_file.write_text('[photo-cli]\ndescription = "from config"\n', encoding="utf-8")

    calls = {}

    monkeypatch.setattr(main, "ensure_exiftool", lambda: None)
    monkeypatch.setattr(main, "find_files", lambda patterns: [Path("sample.jpg")])
    monkeypatch.setattr(
        main,
        "write_metadata",
        lambda files, description: calls.setdefault("description", description),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["photo-cli", "meta", "--config", str(config_file), "sample.jpg"],
    )

    assert main.main() == 0
    assert calls["description"] == "from config"


def test_meta_cli_description_overrides_config(tmp_path, monkeypatch):
    config_file = tmp_path / "photo-cli.toml"
    config_file.write_text('[photo-cli]\ndescription = "from config"\n', encoding="utf-8")

    calls = {}

    monkeypatch.setattr(main, "ensure_exiftool", lambda: None)
    monkeypatch.setattr(main, "find_files", lambda patterns: [Path("sample.jpg")])
    monkeypatch.setattr(
        main,
        "write_metadata",
        lambda files, description: calls.setdefault("description", description),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "photo-cli",
            "meta",
            "--config",
            str(config_file),
            "--description",
            "from cli",
            "sample.jpg",
        ],
    )

    assert main.main() == 0
    assert calls["description"] == "from cli"
