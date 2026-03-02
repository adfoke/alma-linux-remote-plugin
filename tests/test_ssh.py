from unittest.mock import patch, MagicMock
from src.alma_linux_remote_plugin.ssh import SSHManager
from src.alma_linux_remote_plugin.models import CommandResult, HostConfig, HostAuth

@patch("src.alma_linux_remote_plugin.ssh.load_hosts")
@patch("paramiko.SSHClient")
def test_run_command_success(mock_ssh_client, mock_load_hosts):
    host_config = HostConfig(
        host="127.0.0.1",
        username="testuser",
        auth=HostAuth(method="password", password_env="MY_SERVER_PASS")
    )
    mock_load_hosts.return_value = {"test-server": host_config}

    mock_client = MagicMock()
    mock_ssh_client.return_value = mock_client

    mock_stdout = MagicMock()
    mock_stdout.read.return_value = b"14:30 up 3 days"
    mock_stdout.channel.recv_exit_status.return_value = 0
    mock_stderr = MagicMock()
    mock_stderr.read.return_value = b""

    mock_client.exec_command.return_value = (None, mock_stdout, mock_stderr)

    result = SSHManager.run_command("test-server", "uptime", timeout=10)

    assert isinstance(result, CommandResult)
    assert result.success is True
    assert "14:30 up" in result.stdout

@patch("src.alma_linux_remote_plugin.ssh.load_hosts")
@patch("paramiko.SSHClient")
def test_upload_file(mock_ssh_client, mock_load_hosts):
    host_config = HostConfig(
        host="127.0.0.1",
        username="testuser",
        auth=HostAuth(method="password", password_env="MY_SERVER_PASS")
    )
    mock_load_hosts.return_value = {"test-server": host_config}

    mock_client = MagicMock()
    mock_ssh_client.return_value = mock_client
    mock_sftp = MagicMock()
    mock_client.open_sftp.return_value.__enter__.return_value = mock_sftp

    SSHManager.upload_file("test-server", "/local/file.sh", "/remote/file.sh")

    mock_sftp.put.assert_called_once()
    mock_client.close.assert_called_once()