# -*- coding: utf-8 -*-
"""
Виявлення нестаціонарності (див. §4.6).
"""
import numpy as np

class NonStationarityDetector:
    def __init__(self, cfg):
        self.cfg = cfg
        self.S = None
        self.gamma = 0.2
        self.h = 0.05

    def trigger(self, risk, indexer):
        # Індикація за ризиковими порушеннями (спрощено)
        eps = np.array(risk.eps, dtype=float)
        if self.S is None: self.S = np.zeros_like(eps)
        self.S = np.maximum(0.0, (1-self.gamma)*self.S + eps - 0.0)
        return bool(np.any(self.S >= self.h))
