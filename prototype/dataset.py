import json
from pathlib import Path


class Dataset:
    _instance = None

    def __init__(self):
        dataset_path = Path(__file__).parent.parent / "data" / "cards.json"
        self.dataset: list[dict] = json.loads(dataset_path.read_text())

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_by_id(self, id: int) -> dict:
        return next(c for c in self.dataset if c["id"] == id)
