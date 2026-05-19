import os
import shutil
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config import MAC_ALLOWED_PATHS

router = APIRouter(prefix="/mac", tags=["mac"])


def _resolve(path: str) -> Path:
    p = Path(os.path.expanduser(path)).resolve()
    for allowed in MAC_ALLOWED_PATHS:
        if str(p).startswith(str(Path(allowed).resolve())):
            return p
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
    p = _resolve(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return {"path": str(p), "content": p.read_text(errors="replace")}


@router.post("/write")
def write_file(body: WriteBody):
    p = _resolve(body.path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body.content)
    return {"path": str(p), "status": "written"}


@router.post("/move")
def move_file(body: MoveBody):
    src = _resolve(body.src)
    dst = _resolve(body.dst)
    if not src.exists():
        raise HTTPException(status_code=404, detail="Source not found")
    shutil.move(str(src), str(dst))
    return {"src": str(src), "dst": str(dst), "status": "moved"}


@router.delete("/delete")
def delete_file(body: DeleteBody):
    p = _resolve(body.path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="File not found")
    if p.is_dir():
        shutil.rmtree(str(p))
    else:
        p.unlink()
    return {"path": str(p), "status": "deleted"}


@router.get("/list")
def list_files(path: str):
    p = _resolve(path)
    if not p.exists():
        raise HTTPException(status_code=404, detail="Path not found")
    entries = []
    for item in sorted(p.iterdir()):
        entries.append({"name": item.name, "type": "dir" if item.is_dir() else "file"})
    return {"path": str(p), "entries": entries}
