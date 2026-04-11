import json
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def _ensure_data_dir():
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

def _path(filename):
    name = filename if filename.endswith(".json") else f"{filename}.json"
    return _DATA_DIR / name

def save_data(filename, data):
    _ensure_data_dir()
    with open(_path(filename), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)

def load_data(filename, default=None):
    p = _path(filename)
    if not p.exists():
        return default
    try:
        with open(p, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except:
        return default

def list_saved_files():
    _ensure_data_dir()
    return [f.stem for f in sorted(_DATA_DIR.glob("*.json"))]

def delete_data(filename):
    p = _path(filename)
    if p.exists():
        p.unlink()
        return True
    return False
