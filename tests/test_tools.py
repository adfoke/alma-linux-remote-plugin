from unittest.mock import MagicMock
from src.alma_linux_remote_plugin.tools import (
    list_hosts, test_connection, run_command,
    upload_file, download_file
)
from src.alma_linux_remote_plugin.ssh import SSHManager   # 必须导入原始类

# ====================== test_connection (已彻底修复) ======================
def test_test_connection_success(monkeypatch):
    mock_result = MagicMock()
    mock_result.success = True

    def fake_run(*args, **kwargs):
        return mock_result

    monkeypatch.setattr(SSHManager, "run_command", fake_run)

    result = test_connection("test-server")
    assert "连接成功" in result


def test_test_connection_failure(monkeypatch):
    mock_result = MagicMock()
    mock_result.success = False

    def fake_run(*args, **kwargs):
        return mock_result

    monkeypatch.setattr(SSHManager, "run_command", fake_run)

    result = test_connection("test-server")
    assert "连接失败" in result


# ====================== 其他测试 ======================
def test_run_command(monkeypatch):
    mock_result = MagicMock()

    def fake_run(*args, **kwargs):
        return mock_result

    monkeypatch.setattr(SSHManager, "run_command", fake_run)

    result = run_command("test-server", "ls")
    assert result == mock_result


def test_upload_file(monkeypatch):
    def fake_upload(*args, **kwargs):
        pass
    monkeypatch.setattr(SSHManager, "upload_file", fake_upload)

    result = upload_file("test-server", "local.sh", "/tmp/remote.sh")
    assert "上传成功" in result


def test_download_file(monkeypatch):
    def fake_download(*args, **kwargs):
        pass
    monkeypatch.setattr(SSHManager, "download_file", fake_download)

    result = download_file("test-server", "/remote.sh", "local.sh")
    assert "下载成功" in result


def test_list_hosts(monkeypatch):
    mock_hosts = {"test-server": None}
    monkeypatch.setattr(
        "src.alma_linux_remote_plugin.tools.load_hosts",
        lambda: mock_hosts
    )
    assert list_hosts() == ["test-server"]