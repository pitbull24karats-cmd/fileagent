import io
import paramiko
from config import SSH_HOST, SSH_USER, SSH_KEY_PATH


def _get_client() -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(SSH_HOST, username=SSH_USER, key_filename=SSH_KEY_PATH, timeout=10)
    return client


def ssh_read(path: str) -> str:
    client = _get_client()
    try:
        sftp = client.open_sftp()
        with sftp.file(path, "r") as f:
            return f.read().decode("utf-8", errors="replace")
    finally:
        client.close()


def ssh_write(path: str, content: str) -> None:
    client = _get_client()
    try:
        sftp = client.open_sftp()
        with sftp.file(path, "w") as f:
            f.write(content.encode("utf-8"))
    finally:
        client.close()


def ssh_move(src: str, dst: str) -> None:
    client = _get_client()
    try:
        sftp = client.open_sftp()
        sftp.rename(src, dst)
    finally:
        client.close()


def ssh_delete(path: str) -> None:
    client = _get_client()
    try:
        sftp = client.open_sftp()
        sftp.remove(path)
    finally:
        client.close()


def ssh_list(path: str) -> list[str]:
    client = _get_client()
    try:
        sftp = client.open_sftp()
        return sftp.listdir(path)
    finally:
        client.close()


def ssh_exec(command: str) -> tuple[str, str]:
    client = _get_client()
    try:
        _, stdout, stderr = client.exec_command(command, timeout=30)
        return stdout.read().decode(), stderr.read().decode()
    finally:
        client.close()
