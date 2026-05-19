import subprocess
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/build", tags=["build"])

_last_build: dict = {}


class XcodeBody(BaseModel):
    scheme: str
    destination: str = "generic/platform=iOS"
    project_path: str = ""


class LaunchctlBody(BaseModel):
    action: str  # load | unload | start | stop | restart
    service: str


@router.post("/xcode")
def xcode_build(body: XcodeBody):
    cmd = ["xcodebuild", "-scheme", body.scheme, "-destination", body.destination]
    if body.project_path:
        cmd += ["-project", body.project_path]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    _last_build["returncode"] = result.returncode
    _last_build["stdout"] = result.stdout[-3000:]
    _last_build["stderr"] = result.stderr[-2000:]
    if result.returncode != 0:
        raise HTTPException(status_code=500, detail=result.stderr[-500:])
    return {"status": "success", "output": result.stdout[-500:]}


@router.post("/launchctl")
def launchctl_op(body: LaunchctlBody):
    action = body.action.lower()
    if action not in ("load", "unload", "start", "stop", "restart"):
        raise HTTPException(status_code=400, detail="Invalid action")
    if action == "restart":
        subprocess.run(["launchctl", "stop", body.service], capture_output=True)
        result = subprocess.run(["launchctl", "start", body.service], capture_output=True, text=True)
    else:
        result = subprocess.run(["launchctl", action, body.service], capture_output=True, text=True)
    return {"action": action, "service": body.service, "returncode": result.returncode, "output": result.stdout + result.stderr}


@router.get("/status")
def build_status():
    return _last_build if _last_build else {"status": "no build yet"}
