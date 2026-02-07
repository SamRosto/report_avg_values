# Запуск проекта

<!-- ```bash -->
`git clone git@github.com:SamRosto/report_avg_values.git`
<!-- ```bash -->
`cd report_avg_values`
---
<!-- ```bash -->
`uv init && uv sync`

# Запуск тестов
**Базовые тесты:**
<!-- ```bash -->
`uv run pytest tests/ -v`

**Покрытие:**
<!-- ```bash -->
`uv run pytest --cov=main --cov-report=term-missing tests/`

# Запуск скрипта
<!-- ```bash -->
`uv run main.py --files economic1.csv economic2.csv --report average-gdp`

* Введите название колонки: `gdp`

<div align="center">
  <h2>Итоговый результат</h2>
  <img src="https://github.com/SamRosto/report_avg_values/raw/main/images/result_table.png" width="300">
  <h3>Таблица средних показателей по странам из CSV</h3>
</div>