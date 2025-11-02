# -*- coding: utf-8 -*-
"""
Журнал подій і рішень (див. §4.8.3).
"""
import json, io, os, numpy as np

class NumpyEncoder(json.JSONEncoder):
    """Дозволяє серіалізацію numpy типів."""
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return super().default(obj)

class Journal:
    def __init__(self, path):
        self.path = path
        self.f = io.open(self.path, "w", encoding="utf-8")

    def write(self, rec: dict):
        self.f.write(json.dumps(rec, ensure_ascii=False, cls=NumpyEncoder) + "\n")
        self.f.flush()

    def close(self):
        try:
            self.f.close()
        except Exception:
            pass
