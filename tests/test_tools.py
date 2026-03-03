from unittest.mock import MagicMock

from alma_linux_remote_plugin.tools import (
    download_file,
    list_hosts,
    run_command,
    test_connection as tool_test_connection,
    upload_file,
)


def test_test_connection_success(monkeypatch):
    mock_result = MagicMock()
    mock_result.success = True
    monkeypatch.setattr(
        "alma_linux_remote_plugin.tools.SessionManager.run_command",
        lambda *args, **kwargs: mock_result,
    )

    result = tool_test_connection("test-server")
    assert "连接成功" in result


def test_test_connection_failure(monkeypatch):
    mock_result = MagicMock()
    mock_result.success = False
    monkeypatch.setattr(
        "alma_linux_remote_plugin.tools.SessionManager.run_command",
        lambda *args, **kwargs: mock_result,
    )

    result = tool_test_connection("test-server")
    assert "连接失败" in result


def test_test_connection_exception(monkeypatch):
    def raise_exc(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr("alma_linux_remote_plugin.tools.SessionManager.run_command", raise_exc)
    result = tool_test_connection("test-server")
    assert "连接异常" in result


def test_run_command(monkeypatch):
    mock_result = MagicMock()
    monkeypatch.setattr(
        "alma_linux_remote_plugin.tools.SessionManager.run_command",
        lambda *args, **kwargs: mock_result,
    )

    result = run_command("test-server", "ls")
    assert result == mock_result


def test_upload_file(monkeypatch):
    monkeypatch.setattr(
        "alma_linux_remote_plugin.tools.SessionManager.upload_file",
        lambda *args, **kwargs: "上传成功 local.sh → /tmp/remote.sh",
    )

    result = upload_file("test-server", "local.sh", "/tmp/remote.sh")
    assert "上传成功" in result


def test_download_file(monkeypatch):
    monkeypatch.setattr(
        "alma_linux_remote_plugin.tools.SessionManager.download_file",
        lambda *args, **kwargs: "下载成功 /remote.sh → local.sh",
    )

    result = download_file("test-server", "/remote.sh", "local.sh")
    assert "下载成功" in result


def test_list_hosts(monkeypatch):
    monkeypatch.setattr(
        "alma_linux_remote_plugin.tools.load_hosts",
        lambda: {"test-server": object()},
    )
    assert list_hosts() == ["test-server"]
