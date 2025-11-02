# -*- coding: utf-8 -*-
"""
Двоконтурне налаштування (див. §4.5).
"""
import numpy as np

class FastAdaptor:
    def __init__(self, cfg):
        self.cfg = cfg
        self.eta = float(cfg["adapt"]["fast"]["eta"])
        self.tau_down = float(cfg["adapt"]["fast"]["tau_down"])
        self.tau_up = float(cfg["adapt"]["fast"]["tau_up"])
        self.s5_min = float(cfg["adapt"]["fast"]["s5_min"])
        self.s5_max = float(cfg["adapt"]["fast"]["s5_max"])

    def step(self, indexer, risk):
        # R(t) = sum w*eps / sum w*delta  (демо версія)
        num = float(np.dot(risk.w_risk, risk.eps))
        den = float(np.dot(risk.w_risk, risk.delta) + 1e-9)
        R = num/den if den>0 else 0.0

        # лінійна мертва зона
        if R <= self.tau_down:
            target = self.s5_min
        elif R >= self.tau_up:
            target = self.s5_max
        else:
            a = (R - self.tau_down) / max(1e-9, (self.tau_up - self.tau_down))
            target = self.s5_min + a*(self.s5_max - self.s5_min)

        # оновити alpha5 з амортизацією
        indexer.alpha5 = (1.0 - self.eta)*indexer.alpha5 + self.eta*target

    def stabilize(self, risk, indexer):
        # консервативна дія при нестаціонарності
        indexer.alpha5 = min(self.s5_max, indexer.alpha5 + 0.05)


class SlowAdaptor:
    def __init__(self, cfg):
        self.cfg = cfg
        self.mu = float(cfg["adapt"]["slow"]["mu"])

    def recalibrate(self, indexer, risk):
        # Демоверсія: легке повернення до рівної базової пропорції
        base = np.array(indexer.alpha_base, dtype=float)
        base = (1-self.mu)*base + self.mu*(np.ones_like(base)/len(base))
        indexer.alpha_base = base
