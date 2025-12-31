"""Checkpoint management for ingestion pipeline."""
import json
from pathlib import Path
from datetime import datetime

class CheckpointManager:
    def __init__(self, checkpoint_file: str = "checkpoints.json"):
        self.file = Path(checkpoint_file)
        self.data = self._load()
    
    def _load(self):
        if self.file.exists():
            with open(self.file) as f:
                return json.load(f)
        return {}
    
    def save_checkpoint(self, source: str, count: int):
        self.data[source] = {"count": count, "last_updated": datetime.utcnow().isoformat()}
        self.file.parent.mkdir(exist_ok=True)
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=2)
