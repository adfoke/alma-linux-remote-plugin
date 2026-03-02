import pytest
from pathlib import Path
import yaml
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch, tmp_path: Path):
    """每次测试自动创建 hosts.yaml 并切换目录"""
    load_dotenv()
    monkeypatch.setenv("MY_SERVER_PASS", "test_password_123")
    monkeypatch.chdir(tmp_path)   # 关键：让 load_hosts() 找到临时文件

    hosts_file = tmp_path / "hosts.yaml"
    data = {
        "hosts": {
            "test-server": {
                "host": "127.0.0.1",
                "username": "testuser",
                "auth": {
                    "method": "password",
                    "password_env": "MY_SERVER_PASS"
                }
            }
        }
    }
    hosts_file.write_text(yaml.dump(data), encoding="utf-8")
    yield