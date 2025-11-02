# -*- coding: utf-8 -*-
"""
Головний модуль запуску експерименту (див. §4.8).
"""
import argparse, yaml, os, random, numpy as np
from .scenario_generators import generate_events
from .event_loop import EventEngine
from .journal import Journal

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="experiments/demo_run/config.yaml")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    seed = int(cfg.get("scenario",{}).get("seed", 123))
    random.seed(seed); np.random.seed(seed)

    # Журнал
    os.makedirs("data", exist_ok=True)
    journal_path = "data/demo_event_log.jsonl"
    journal = Journal(journal_path)

    # Генерація подій
    events = generate_events(cfg)

    # Двигун подієвого алгоритму
    engine = EventEngine(cfg, journal)

    # Основний цикл
    for ev in events:
        engine.process_event(ev)

    journal.close()
    print(f"[OK] Журнал збережено: {journal_path}")

if __name__ == "__main__":
    main()
