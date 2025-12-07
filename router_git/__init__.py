from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from arcreactor.core.interfaces.plugin import RouterPlugin
import logging

logger = logging.getLogger(__name__)

class GitStatusResponse(BaseModel):
    output: str
    error: Optional[str] = None

class GitControlPlugin(RouterPlugin):
    def __init__(self, manifest, context):
        super().__init__(manifest, context)
        self.router = APIRouter(prefix="/git", tags=["git"])
        self._setup_routes()

    def _setup_routes(self):
        @self.router.get("/status", response_model=GitStatusResponse)
        async def git_status(cwd: str = "."):
            """
            Runs 'git status' in the specified directory.
            """
            if hasattr(self.context, "state") and hasattr(self.context.state, "subprocess_launcher"):
                launcher = self.context.state.subprocess_launcher
                code, stdout, stderr = await launcher.run("git status", cwd=cwd)
                if code != 0:
                    return GitStatusResponse(output=stdout, error=stderr)
                return GitStatusResponse(output=stdout)
            else:
                raise HTTPException(status_code=503, detail="SubprocessLauncher not available")

    async def initialize(self):
        logger.info("GitControlPlugin initialized.")

    async def shutdown(self):
        pass

    def get_router(self):
        return self.router
