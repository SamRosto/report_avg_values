# Запуск проекта
---
`git clone git@github.com:SamRosto/report_avg_values.git`
`cd report_avg_values`
---
`uv init && uv sync`

# Запуск тестов
`uv run pytest tests/ -v`
`uv run pytest --cov=main --cov-report=term-missing tests/`

# Запуск скрипта
`uv run main.py --files economic1.csv economic2.csv --report average-gdp`

* Введите название колонки: `gdp`

<div align="center">
  <img src="https://github.com/SamRosto/report_avg_values/raw/main/images/result_table.png" width="200">
  <h3>Таблица средних показателей по странам из CSV</h3>
</div>