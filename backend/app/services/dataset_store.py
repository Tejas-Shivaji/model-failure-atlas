from collections import OrderedDict
from threading import RLock
from uuid import uuid4
import pandas as pd

# Bounded process memory store: suitable for a single local/demo worker.
# Data is intentionally not durable; saved investigation summaries are durable.
_MAX_DATASETS = 8
_STORE = OrderedDict()
_LOCK = RLock()

def put_dataset(name: str, frame: pd.DataFrame) -> str:
    dataset_id = str(uuid4())
    with _LOCK:
        _STORE[dataset_id] = {"name": name, "frame": frame.copy()}
        while len(_STORE) > _MAX_DATASETS:
            _STORE.popitem(last=False)
    return dataset_id

def get_dataset(dataset_id: str):
    with _LOCK:
        item = _STORE.get(dataset_id)
        if item is None:
            return None
        _STORE.move_to_end(dataset_id)
        return item

def clear_datasets():
    with _LOCK:
        _STORE.clear()
