import subprocess
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/git", tags=["git"])


def _run(cmd: list[str], cwd: str) -> str:
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr.strip())
    return result.stdout.strip()


class AddBody(BaseModel):
    path: str = "."
    cwd: str


class CommitBody(BaseModel):
    message: str
    cwd: str


class PushBody(BaseModel):
    cwd: str


class FullBody(BaseModel):
    message: str
    cwd: str


@router.post("/add")
def git_add(body: AddBody):
    out = _run(["git", "add", body.path], body.cwd)
    return {"status": "added", "output": out}


@router.post("/commit")
def git_commit(body: CommitBody):
    out = _run(["git", "commit", "-m", body.message], body.cwd)
    return {"status": "committed", "output": out}


@router.post("/push")
def git_push(body: PushBody):
    out = _run(["git", "push"], body.cwd)
    return {"status": "pushed", "output": out}


@router.post("/full")
def git_full(body: FullBody):
    _run(["git", "add", "."], body.cwd)
    _run(["git", "commit", "-m", body.message], body.cwd)
    out = _run(["git", "push"], body.cwd)
    return {"status": "done", "output": out}


@router.get("/status")
def git_status(cwd: str):
    out = _run(["git", "status"], cwd)
    return {"status": out}


@router.get("/log")
def git_log(cwd: str, limit: int = 10):
    out = _run(["git", "log", f"--oneline", f"-{limit}"], cwd)
    return {"log": out}
