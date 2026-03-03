from pathlib import Path

import pytest
import yaml


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("MY_SERVER_PASS", "test_password_123")
    monkeypatch.chdir(tmp_path)

    hosts_file = tmp_path / "hosts.yaml"
    data = {
        "hosts": {
            "test-server": {
                "host": "127.0.0.1",
                "username": "testuser",
                "auth": {
                    "method": "password",
                    "password_env": "MY_SERVER_PASS",
                },
            }
        },
        "session": {
            "idle_timeout_seconds": 300,
        },
        "audit": {
            "enabled": True,
            "db_path": "./logs/audit.db",
            "dashboard_host": "127.0.0.1",
            "dashboard_port": 8765,
        },
    }
    hosts_file.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    yield
