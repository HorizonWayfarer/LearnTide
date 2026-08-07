"""Base class for platform publishers."""
from abc import ABC, abstractmethod
from pathlib import Path

class PlatformPublisher(ABC):
    def __init__(self, engine):
        self.engine = engine

    @abstractmethod
    def publish(self, content: dict, cover_path: str = None) -> dict:
        """
        Publish content to platform.
        Returns: {"success": bool, "url": str, "error": str}
        """
        pass

    def _checkpoint(self, name: str, page_desc: str = ""):
        """Save screenshot for debugging."""
        shots_dir = Path(__file__).resolve().parent.parent.parent / ".workbuddy" / "preview-shots" / "publish-debug"
        shots_dir.mkdir(parents=True, exist_ok=True)
        path = shots_dir / f"{name}.png"
        self.engine.screenshot(str(path))
        print(f"[checkpoint] {name}: {path} {page_desc}")
        return path
