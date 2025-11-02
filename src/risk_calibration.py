# -*- coding: utf-8 -*-
"""
Імовірнісні обмеження та їх емпіричне калібрування (див. §4.4).
"""
import numpy as np
from .utils import ucb_hoeffding

class RiskCalibrator:
    def __init__(self, cfg):
        self.cfg = cfg
        # три обмеження для демо: 0..2
        self.K = len(cfg["relevance"]["weight_risk"])
        self.w_risk = np.array(cfg["relevance"]["weight_risk"], dtype=float)

        # бюджети ризику δ_k
        dt = float(cfg["risk"]["delta_total"])
        self.delta = np.ones(self.K)*(dt/self.K)
        self.delta_min = float(cfg["risk"]["delta_min"]); self.delta_max = float(cfg["risk"]["delta_max"])

        # статистики порушень
        self.N = 0
        self.v = np.zeros(self.K, dtype=int)  # кількість порушень
        self.alpha = float(cfg["risk"]["alpha_init"])

        # дефіцити ε_k та допоміжні
        self.eps = np.zeros(self.K, dtype=float)
        self.zeta = np.ones(self.K, dtype=float) * 0.5
        self.rho = np.ones(self.K, dtype=float) * 0.01

        # знімок
        self.p_hat_up = np.zeros(self.K, dtype=float)

    def snapshot(self):
        return {
            "p_hat_up": self.p_hat_up.tolist(),
            "delta": self.delta.tolist(),
            "eps": self.eps.tolist(),
        }

    def update_stats(self, violations):
        """violations: бінарний вектор порушень довжини K"""
        self.N += 1
        self.v += np.array(violations, dtype=int)
        # верхня довірча межа
        p_hat = self.v / max(1, self.N)
        self.p_hat_up = p_hat + np.sqrt(np.log(1.0/max(1e-9, self.alpha)) / (2.0*max(1, self.N)))

        # дефіцит ε_k
        self.eps = np.maximum(0.0, self.p_hat_up - self.delta)

    def adjust_set(self, A0, indexer, pool, t):
        """
        Консервативний тест прийнятності та локальні заміни (див. §4.3, §4.4).
        У демо версії тест моделюється через випадкові порушення, щоб показати
        роботу механізму журналювання.
        """
        # Згенеруємо синтетичні порушення для демонстрації
        rng = np.random.default_rng(1234+t)
        violations = (rng.random(self.K) < (self.p_hat_up + 0.05)).astype(int)
        self.update_stats(violations)

        # Нехай A = A0 без замін (щоб код був легким); у повній версії тут би були локальні заміни
        return A0
