# -*- coding: utf-8 -*-
"""
Обчислення індексу (див. §4.2) та нормування ознак (§4.2 Нормування).
"""
import numpy as np

class IndexComputer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.alpha_base = np.array(cfg["index"]["alpha_base"], dtype=float)  # 4 складові
        self.alpha5_bounds = cfg["index"]["alpha5_bounds"]
        self.beta_bounds = cfg["index"]["beta_bounds"]
        self.alpha5 = float(cfg["adapt"]["fast"]["s5_min"])
        self.betas = {}  # per-object bias
        self.hysteresis = float(cfg["index"]["hysteresis"])

        # нормування
        self.q_low = float(cfg["norm"]["quantiles"]["low"])
        self.q_high = float(cfg["norm"]["quantiles"]["high"])

        # релевантності a_{k,u} зберігаємо агреговано на рівні класу
        self.a_ku = {}  # (k,u) -> [0..1]

        # буфери ознак
        self.features = {}  # u -> dict of raw features
        self.normed = {}    # u -> dict of Phi_*

        # список ознак
        self.FEATS = ["prio","stale","load","link","risk"]

        # бюджети ризику (початкові)
        self.delta = None  # встановлюється RiskCalibrator

    def theta_snapshot(self):
        return {"alpha5": self.alpha5}

    def set_delta_vector(self, delta):
        self.delta = np.array(delta, dtype=float)

    # -------- Нормування до [0,1] простим min-max за ковзним буфером (для демо)
    def _norm(self, x, lo, hi, eps=1e-9):
        return float(max(0.0, min(1.0, (x - lo) / (hi - lo + eps))))

    def update_features_and_index(self, ev):
        """
        ev: словник з подією: {u, features:{...}, capacity:C_t, K, ...}
        Повертає множину об'єктів U_t, які змінилися.
        """
        changed = set()

        # оновити features
        for u, feats in ev["features"].items():
            changed.add(u)
            cur = self.features.get(u, {"prio":0.5,"stale":0.0,"load":0.0,"link":1.0,"risk":0.0})
            cur.update(feats)
            self.features[u] = cur

        # нормування і Phi
        # (для простоти беремо робочі межі з конфіга; у повній версії — квантилі)
        qh = self.cfg["norm"]["quantiles"]["high"]
        ql = self.cfg["norm"]["quantiles"]["low"]
        lohi = {
            "prio": (0.0, 1.0),
            "stale": (0.0, 1.0),
            "load": (0.0, 1.0),
            "link": (0.0, 1.0),
            "risk": (0.0, 1.0),
        }
        for u in changed:
            raw = self.features[u]
            self.normed[u] = {k:self._norm(raw.get(k,0.0),*lohi[k]) for k in self.FEATS}

        return changed

    def compute_index(self, u, risk_weight):
        # обчислити ваги 1..4 так, щоб їх сума = (1 - risk_weight)
        base_sum = float(sum(self.alpha_base))
        w = [(1.0-risk_weight) * (a/base_sum) for a in self.alpha_base]
        Phi = self.normed.get(u, {"prio":0.5,"stale":0.0,"load":0.0,"link":1.0,"risk":0.0})
        idx = w[0]*Phi["prio"] + w[1]*Phi["stale"] + w[2]*Phi["load"] + w[3]*Phi["link"] + risk_weight*Phi["risk"]
        beta = float(self.betas.get(u, 0.0))
        return float(idx + beta)
