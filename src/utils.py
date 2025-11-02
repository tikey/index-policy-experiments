# -*- coding: utf-8 -*-
"""
Допоміжні функції (границі Гефдінга, час тощо).
"""
import math, time

def ucb_hoeffding(p_hat: float, N: int, alpha: float) -> float:
    """Верхня довірча межа для біноміальної частоти за нерівністю Гефдінга."""
    if N <= 0: return 1.0
    return min(1.0, p_hat + math.sqrt(math.log(1.0/max(alpha,1e-9)) / (2.0*N)))

def now_ms():
    return int(round(time.time()*1000)) % 1000000
