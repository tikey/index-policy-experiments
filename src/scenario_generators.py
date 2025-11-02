# -*- coding: utf-8 -*-
"""
Генератор подій для демонстрації (переривна зв'язність, «бурстове» навантаження).
"""
import numpy as np

def generate_events(cfg):
    seed = int(cfg["scenario"]["seed"]); rng = np.random.default_rng(seed)
    T = int(cfg["scenario"]["duration_events"])
    n = int(cfg["scenario"]["num_objects"])
    C = int(cfg["capacity"]["C"])
    link_mode = cfg["scenario"]["link_profile"]
    load_mode = cfg["scenario"]["load_profile"]

    events = []
    # базові ряди
    link = np.ones(T)
    if link_mode == "intermittent":
        # простий шаблон on-off
        for t in range(0,T,50):
            link[t:t+25] = 0.0

    load = np.zeros(T)
    if load_mode == "bursty":
        for _ in range(T//100 + 1):
            center = rng.integers(0,T)
            width = rng.integers(10,40)
            amp = rng.uniform(0.4,1.0)
            lo = max(0, center-width); hi=min(T, center+width)
            load[lo:hi] += amp
        load = np.clip(load, 0, 1)

    # ініціалізація об'єктів
    features = {u: {"prio": float(rng.uniform(0.0,1.0)), "stale":0.0, "load":0.0, "link":1.0, "risk":0.0}
                for u in range(n)}

    for t in range(T):
        # оновити "стейлінг" та навантаження
        for u in features.keys():
            features[u]["stale"] = min(1.0, features[u]["stale"] + 0.02 + 0.05*(rng.random()<0.1))
            features[u]["load"]  = min(1.0, 0.3*features[u]["load"] + 0.7*load[t])
            features[u]["link"]  = 1.0 if link[t]>0 else 0.0
            # ризикова компонента — груба імітація напруги за обмеженнями
            features[u]["risk"]  = float(min(1.0, features[u]["risk"]*0.8 + 0.2*(rng.random()<0.2)))

        # вибір підмножини об'єктів, чиї ознаки "оновилися"
        updated = {u: features[u] for u in np.random.choice(list(features.keys()), size=min(10,n), replace=False)}

        ev = {
            "t": t+1,
            "capacity": C,
            "features": updated
        }
        events.append(ev)
    return events
