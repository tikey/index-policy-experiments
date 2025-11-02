# Чек-лист відтворюваності

1) Зафіксувати версію Python і `pip freeze > docs/requirements.lock`.
2) Встановити залежності: `pip install -r requirements.txt`.
3) Задати значення генератора у конфігурації (`scenario.seed`).
4) Запустити `python -m src.main --config experiments/demo_run/config.yaml`.
5) Перевірити, що згенеровано файл журналу `data/demo_event_log.jsonl`.
6) Побудувати графіки: `python scripts/make_plots.py --journal data/demo_event_log.jsonl --out data/figures`.
7) Перевірити співпадіння ключових метрик у допустимих довірчих межах.
