from unittest.mock import patch, MagicMock
from src.alma_linux_remote_plugin.runtime_adapter import adapter

def test_get_tools():
    tools = adapter.get_tools()
    assert len(tools) == 5

@patch("src.alma_linux_remote_plugin.tools.list_hosts")
def test_invoke_list_hosts(mock_list_hosts):
    mock_list_hosts.return_value = ["test-server"]
    result = adapter.invoke("list_hosts", {})
    assert result == ["test-server"]

@patch("src.alma_linux_remote_plugin.ssh.SSHManager.run_command")   # ← 关键修复：patch 最底层
def test_invoke_run_command(mock_run_command):
    mock_result = MagicMock()
    mock_result.model_dump.return_value = {
        "command": "uptime",
        "exit_code": 0,
        "stdout": "14:30 up ...",
        "stderr": "",
        "success": True
    }
    mock_run_command.return_value = mock_result

    result = adapter.invoke("run_command", {
        "host_name": "test-server",
        "command": "uptime"
    })
    assert result["success"] is True
    mock_run_command.assert_called_once()