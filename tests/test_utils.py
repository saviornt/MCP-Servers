import subprocess
import platform

import pytest
from get_system_resources.utils import (
    has_command,
    human_readable_size,
    gb,
    run_cmd,
    is_windows,
    is_linux,
    is_macos,
)


def test_human_readable_size_bytes_and_units():
    assert human_readable_size(512).unit == "B"
    assert human_readable_size(2048).unit == "KB"
    assert human_readable_size(2 * 1024**2).unit == "MB"
    assert human_readable_size(3 * 1024**3).unit == "GB"


def test_gb_converts_bytes_to_gigabytes():
    assert gb(1024**3) == 1.0
    assert gb(1536 * 1024**2) == 1.5


def test_run_cmd_returns_output(monkeypatch):
    monkeypatch.setattr(subprocess, "check_output", lambda *args, **kwargs: "ok")
    assert run_cmd(["echo"]) == "ok"


def test_run_cmd_returns_empty_on_failure(monkeypatch):
    def raise_error(*args, **kwargs):
        raise subprocess.CalledProcessError(returncode=1, cmd=args[0])

    monkeypatch.setattr(subprocess, "check_output", raise_error)
    assert run_cmd(["false"]) == ""


@pytest.mark.parametrize(
    "system_name,expected",
    [
        ("Windows", (True, False, False)),
        ("Linux", (False, True, False)),
        ("Darwin", (False, False, True)),
    ],
)
def test_platform_helpers(monkeypatch, system_name, expected):
    monkeypatch.setattr(platform, "system", lambda: system_name)
    assert is_windows() == expected[0]
    assert is_linux() == expected[1]
    assert is_macos() == expected[2]


def test_has_command_uses_shutil_which(monkeypatch):
    monkeypatch.setattr(
        "shutil.which", lambda cmd: "/usr/bin/python" if cmd == "python" else None
    )
    assert has_command("python") is True
    assert has_command("nope") is False
