from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import WIN_ALLOWED_PATHS
from services import ssh_client

router = APIRouter(prefix="/win", tags=["win"])


def _check_path(path: str) -> str:
    normalized = path.replace("/", "\\")
    for allowed in WIN_ALLOWED_PATHS:
        if normalized.startswith(allowed):
            return normalized
    raise HTTPException(status_code=403, detail=f"Path not allowed: {path}")


class WriteBody(BaseModel):
    path: str
    content: str


class MoveBody(BaseModel):
    src: str
    dst: str


class DeleteBody(BaseModel):
    path: str


@router.get("/read")
def read_file(path: str):
    p = _check_path(path)
    try:
        content = ssh_client.ssh_read(p)
        return {"path": p, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/write")
def write_file(body: WriteBody):
    p = _check_path(body.path)
    try:
        ssh_client.ssh_write(p, body.content)
        return {"path": p, "status": "written"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/move")
def move_file(body: MoveBody):
    src = _check_path(body.src)
    dst = _check_path(body.dst)
    try:
        ssh_client.ssh_move(src, dst)
        return {"src": src, "dst": dst, "status": "moved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete")
def delete_file(body: DeleteBody):
    p = _check_path(body.path)
    try:
        ssh_client.ssh_delete(p)
        return {"path": p, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
def list_files(path: str):
    p = _check_path(path)
    try:
        entries = ssh_client.ssh_list(p)
        return {"path": p, "entries": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
