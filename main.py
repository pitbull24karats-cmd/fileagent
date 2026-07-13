import logging
import httpx
from fastapi import FastAPI
from routers import mac_files, win_files, git_ops, build, codegen
from config import OLLAMA_URL, SSH_HOST

logger = logging.getLogger(__name__)

app = FastAPI(title="FileAgent", version="1.0.0")

app.include_router(mac_files.router)
app.include_router(win_files.router)
app.include_router(git_ops.router)
app.include_router(build.router)
app.include_router(codegen.router)


@app.get("/health")
async def health():
    status = {"server": "ok", "ollama": "unreachable", "ssh": "unchecked"}

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            if resp.status_code == 200:
                status["ollama"] = "ok (windows)"
    except Exception as e:
        logger.error(f"Ollama(Windows: {OLLAMA_URL})に接続できません: {e}")
        status["ollama"] = "unreachable"

    try:
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        from config import SSH_USER, SSH_KEY_PATH
        client.connect(SSH_HOST, username=SSH_USER, key_filename=SSH_KEY_PATH, timeout=5)
        client.close()
        status["ssh"] = "ok"
    except Exception as e:
        status["ssh"] = f"error: {e}"

    return status
