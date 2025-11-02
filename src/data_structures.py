# -*- coding: utf-8 -*-
"""
Пріоритетні структури даних (див. §4.3, §4.7). Для демо — мінімальна реалізація.
"""
import heapq

class PriorityPool:
    def __init__(self, C):
        self.C = int(C)
        self.heap = []

    def top_k(self, indexer, changed):
        # Для демо: оцінити індекс для всіх відомих об'єктів і обрати top-C
        vals = []
        for u in indexer.features.keys():
            idx = indexer.compute_index(u, indexer.alpha5)
            vals.append((idx, u))
        vals.sort(reverse=True)
        top = [u for _,u in vals[:self.C]]
        return top
