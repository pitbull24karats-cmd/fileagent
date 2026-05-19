import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ollama_client import generate_code

router = APIRouter(prefix="/codegen", tags=["codegen"])


class GenerateBody(BaseModel):
    prompt: str
    language: str = ""
    context: str = ""


class ModifyBody(BaseModel):
    path: str
    instruction: str


class ReviewBody(BaseModel):
    path: str


@router.post("/generate")
async def codegen_generate(body: GenerateBody):
    try:
        result = await generate_code(body.prompt, body.language, body.context)
        return {"code": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/modify")
async def codegen_modify(body: ModifyBody):
    p = Path(os.path.expanduser(body.path))
    if not p.exists():
        raise HTTPException(status_code=404, detail="File not found")
    existing = p.read_text(errors="replace")
    prompt = f"Modify the following code according to the instruction.\n\nInstruction: {body.instruction}\n\nCode:\n{existing}"
    try:
        result = await generate_code(prompt)
        return {"path": str(p), "code": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/review")
async def codegen_review(body: ReviewBody):
    p = Path(os.path.expanduser(body.path))
    if not p.exists():
        raise HTTPException(status_code=404, detail="File not found")
    existing = p.read_text(errors="replace")
    prompt = f"Review the following code. Point out bugs, security issues, and improvements:\n\n{existing}"
    try:
        result = await generate_code(prompt)
        return {"path": str(p), "review": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
