from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel


class HostAuth(BaseModel):
    method: Literal["password", "key"]
    password_env: Optional[str] = None
    key_path: Optional[str] = None
    passphrase_env: Optional[str] = None


class HostConfig(BaseModel):
    host: str
    port: int = 22
    username: str
    auth: HostAuth


class CommandResult(BaseModel):
    command: str
    exit_code: int
    stdout: str
    stderr: str
    success: bool


class SessionConfig(BaseModel):
    idle_timeout_seconds: int = 300


class AuditConfig(BaseModel):
    enabled: bool = True
    db_path: str = "./logs/audit.db"
    dashboard_host: str = "127.0.0.1"
    dashboard_port: int = 8765


class PluginConfig(BaseModel):
    session: SessionConfig = SessionConfig()
    audit: AuditConfig = AuditConfig()
