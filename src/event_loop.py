# -*- coding: utf-8 -*-
"""
Подієва обробка (див. §4.3) з мінімальною реалізацією.
"""
from .index_policy import IndexComputer
from .risk_calibration import RiskCalibrator
from .adapt import FastAdaptor, SlowAdaptor
from .detectors import NonStationarityDetector
from .data_structures import PriorityPool
from .utils import now_ms

class EventEngine:
    def __init__(self, cfg, journal):
        self.cfg = cfg
        self.journal = journal

        self.indexer = IndexComputer(cfg)
        self.risk = RiskCalibrator(cfg)
        self.fast = FastAdaptor(cfg)
        self.slow = SlowAdaptor(cfg)
        self.det = NonStationarityDetector(cfg)

        C = int(cfg.get("capacity",{}).get("C", 1))
        self.pool = PriorityPool(C)

        self.t = 0
        self.events_since_slow = 0

    def process_event(self, ev):
        self.t += 1
        # 1) оновлення ознак, нормування, індекси
        changed = self.indexer.update_features_and_index(ev)

        # 2) попередній вибір top-C
        A0 = self.pool.top_k(self.indexer, changed)

        # 3) ризик-тест і локальні заміни
        A = self.risk.adjust_set(A0, self.indexer, self.pool, self.t)

        # 4) швидка адаптація ваг
        self.fast.step(self.indexer, self.risk)

        # 5) нестаціонарність і стабілізація
        if self.det.trigger(self.risk, self.indexer):
            self.fast.stabilize(self.risk, self.indexer)

        # 6) повільна рекалібровка
        self.events_since_slow += 1
        if self.events_since_slow >= int(self.cfg["adapt"]["slow"]["dT_events"]):
            self.slow.recalibrate(self.indexer, self.risk)
            self.events_since_slow = 0

        # 7) журналювання (мінімальний набір полів)
        self.journal.write({
            "t": self.t,
            "act": list(A),
            "stats": self.risk.snapshot(),
            "theta": self.indexer.theta_snapshot(),
            "cost": {"step_ms": now_ms() % 7 + 1}  # імітація вартості на крок
        })
