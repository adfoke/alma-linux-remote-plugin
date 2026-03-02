import pytest
from src.alma_linux_remote_plugin.config import load_hosts

def test_load_hosts_success():
    """正常加载 hosts.yaml（conftest 已自动提供）"""
    hosts = load_hosts()
    assert "test-server" in hosts
    assert hosts["test-server"].host == "127.0.0.1"
    assert hosts["test-server"].auth.method == "password"

def test_load_hosts_file_not_found():
    """测试文件不存在时抛出正确异常"""
    with pytest.raises(FileNotFoundError, match="hosts 文件不存在"):
        load_hosts(config_path="/non/existent/hosts.yaml")