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


def test_write_metadata_uses_utf8_charset(monkeypatch):
    captured = {}

    def fake_run(args, check):
        captured["args"] = args
        captured["check"] = check

    monkeypatch.setattr(main.subprocess, "run", fake_run)

    main.write_metadata([Path("sample.jpg")], "黒部峡谷トロッコ電車")

    assert captured["args"][0:6] == [
        "exiftool",
        "-overwrite_original",
        "-charset",
        "UTF8",
        "-charset",
        "IPTC=UTF8",
    ]
    assert captured["check"] is True
