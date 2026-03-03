from __future__ import annotations

from typing import Any, Dict, List

from .models import CommandResult
from .tools import download_file, list_hosts, run_command, test_connection, upload_file


class AlmaRuntimeAdapter:
    def get_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_hosts",
                    "description": "列出所有可用 Linux 主机",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "test_connection",
                    "description": "测试主机连通性（复用或创建持久会话）",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "host_name": {"type": "string"},
                            "timeout": {"type": "integer", "default": 15},
                        },
                        "required": ["host_name"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_command",
                    "description": "在持久会话中执行命令",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "host_name": {"type": "string"},
                            "command": {"type": "string"},
                            "timeout": {"type": "integer", "default": 60},
                        },
                        "required": ["host_name", "command"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "upload_file",
                    "description": "上传文件到远程主机",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "host_name": {"type": "string"},
                            "local_path": {"type": "string"},
                            "remote_path": {"type": "string"},
                        },
                        "required": ["host_name", "local_path", "remote_path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "download_file",
                    "description": "从远程主机下载文件",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "host_name": {"type": "string"},
                            "remote_path": {"type": "string"},
                            "local_path": {"type": "string"},
                        },
                        "required": ["host_name", "remote_path", "local_path"],
                    },
                },
            },
        ]

    def invoke(self, tool_name: str, args: Dict[str, Any]) -> Any:
        if tool_name == "list_hosts":
            return list_hosts()
        if tool_name == "test_connection":
            return test_connection(args["host_name"], args.get("timeout", 15))
        if tool_name == "run_command":
            result: CommandResult = run_command(
                args["host_name"], args["command"], args.get("timeout", 60)
            )
            return result.model_dump()
        if tool_name == "upload_file":
            return upload_file(args["host_name"], args["local_path"], args["remote_path"])
        if tool_name == "download_file":
            return download_file(args["host_name"], args["remote_path"], args["local_path"])
        raise ValueError(f"未知工具: {tool_name}")


adapter = AlmaRuntimeAdapter()


def get_tools():
    return adapter.get_tools()


def invoke(tool_name: str, args: Dict[str, Any]):
    return adapter.invoke(tool_name, args)
