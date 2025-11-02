# Репозиторій експериментів: Метод синтезу індексних політик

Цей репозиторій містить мінімально достатню реалізацію та артефакти для відтворення експериментів у рамках дослідження "МЕТОД СИНТЕЗУ ІНДЕКСНИХ ПОЛІТИК ДЛЯ ЗАБЕЗПЕЧЕННЯ ЖИВУЧОСТІ ІНФОРМАЦІЙНОЇ СИСТЕМИ НА МОБІЛЬНІЙ ПЛАТФОРМІ".
Код не використовує специфічних модельних конструкцій з інших наукових публікацій і зосереджений саме на **методі** (індексне правило, імовірнісні обмеження, двоконтурне налаштування, виявлення нестаціонарності).

## Швидкий старт
```bash
# 1) (опційно) створити віртуальне середовище
# python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) запустити демо-експеримент
python -m src.main --config experiments/demo_run/config.yaml

# 3) побудувати базові графіки
python scripts/make_plots.py --journal data/demo_event_log.jsonl --out data/figures
```

## Структура
```
index-policy-experiments/
├─ README.md
├─ LICENSE
├─ requirements.txt
├─ config/
│  └─ default.yaml
├─ experiments/
│  └─ demo_run/
│     └─ config.yaml
├─ src/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ event_loop.py
│  ├─ index_policy.py
│  ├─ risk_calibration.py
│  ├─ adapt.py
│  ├─ detectors.py
│  ├─ data_structures.py
│  ├─ journal.py
│  ├─ scenario_generators.py
│  └─ utils.py
├─ scripts/
│  ├─ run_experiment.sh
│  └─ make_plots.py
├─ data/
│  ├─ demo_event_log.jsonl
│  └─ figures/  (створиться під час побудови графіків)
└─ docs/
   ├─ CHECKLIST.md
   └─ FIGURE_MAP.md
```

## Примітки
- Мова коду: Python 3.10+
- Коментарі та документація: українською, можлива адаптація англійською.
- Графіки будує `matplotlib` (без стилів/заданих кольорів). Графіки підлягають адаптації згідно з вимог видання, в якому буде публікуватися дане дослідження.
