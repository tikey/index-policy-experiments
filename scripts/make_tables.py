# -*- coding: utf-8 -*-
"""
Генерація таблиць основних показників з журналу подій
(для розділу 5 — верифікація властивостей методу)
"""
import json, pandas as pd, numpy as np

journal_path = "data/demo_event_log.jsonl"
records = [json.loads(line) for line in open(journal_path, encoding="utf-8")]

# Зведення по k=0 (першому обмеженню)
p_up = [r["stats"]["p_hat_up"][0] for r in records]
delta = [r["stats"]["delta"][0] for r in records]
eps = [r["stats"]["eps"][0] for r in records]
alpha5 = [r["theta"]["alpha5"] for r in records]

df = pd.DataFrame({
    "t": [r["t"] for r in records],
    "p_up": p_up,
    "delta": delta,
    "eps": eps,
    "alpha5": alpha5
})

summary = pd.DataFrame({
    "metric": ["p_up", "delta", "eps", "alpha5"],
    "mean": [df["p_up"].mean(), df["delta"].mean(), df["eps"].mean(), df["alpha5"].mean()],
    "std": [df["p_up"].std(), df["delta"].std(), df["eps"].std(), df["alpha5"].std()],
    "min": [df["p_up"].min(), df["delta"].min(), df["eps"].min(), df["alpha5"].min()],
    "max": [df["p_up"].max(), df["delta"].max(), df["eps"].max(), df["alpha5"].max()]
})

summary.to_csv("data/summary_metrics.csv", index=False, encoding="utf-8-sig")
print("✅ Збережено таблицю: data/summary_metrics.csv")
