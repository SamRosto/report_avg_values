import csv
import argparse
from tabulate import tabulate
from collections import defaultdict


def parse_args():
    parser = argparse.ArgumentParser(description='Mean GDP by country')
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--report", required=True)
    return parser.parse_args()


def get_available_columns(file_path: str) -> list[str]:
    """Shows available columns in the file"""
    with open(file_path, 'r', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or []


def get_row(reader, row_val: str):
    try:
        return next(key for key in reader.fieldnames if key.casefold() == row_val.casefold())
    except StopIteration:
        return None


def column_select(files: list[str]) -> str:
    """Column Picker"""
    print("\n📋 Доступные колонки в файлах:")
    
    cat_columns = ['country', 'year', 'continent']
    all_columns = set()

    for file_path in files:
        columns = get_available_columns(file_path)
        print(f"  {file_path}: {', '.join(columns)}")
        all_columns.update(set(columns) - set(cat_columns))
    
    while True:
        print(f"\nВыберите колонку для расчёта (из: {', '.join(sorted(all_columns))}):")
        calc_by = input("Введите название колонки: ").strip()

        if calc_by not in cat_columns:
            # Проверяем во всех файлах
            valid_in_all = True
            for file_path in files:
                columns = get_available_columns(file_path)
                if calc_by.casefold() not in [c.casefold() for c in columns]:
                    print(f"🔴 Колонка '{calc_by}' НЕ найдена в {file_path}")
                    valid_in_all = False
                    break
            
            if valid_in_all:
                print(f"🟢 Выбрана колонка '{calc_by}'")
                return calc_by
            else:
                print(f"🔄 Попробуйте снова. Возможно вы ошиблись в названии. Ваш выбор: {calc_by}")
        else:
            print(f"🔄 Попробуйте снова. {calc_by} не в списке возможных колонок для расчета")


def read_from_csv(files: list[str], calc_by: str) -> dict[str, list[str]]:
    """Loads data"""
    gdp_by_country = defaultdict(list)
    
    for file_path in files:
        with open(file_path, 'r', encoding='UTF-8') as f:
            reader = csv.DictReader(f)
            row_key = get_row(reader, calc_by)
            
            if row_key is None:
                print(f"🟡 Пропускаем {file_path} (нет колонки {calc_by})")
                continue
            
            for row in reader:
                country = row.get('country', row.get('Country', 'Unknown'))
                try:
                    gdp_by_country[country].append(row[row_key])
                except KeyError:
                    continue
    
    return gdp_by_country


def mean_gdp_calculate(data: dict[str, list[str]]) -> dict[str, float]:
    """Calculates average per country"""
    d = {}
    for k, v in data.items():
        if v:  # Проверка, что список не пустой
            res = round(sum(float(x) for x in v) / len(v), 2)
            d[k] = res
    return d


def draw_table(table: dict[str, float], calc_by: str, report: str) -> None:
    """Draws final table"""
    sorted_table = dict(sorted(table.items(), key=lambda x: x[1], reverse=True))
    table_data = [[country, f"{gdp:,.2f}"] for country, gdp in sorted_table.items()]
    headers = ["Country", f"Average {calc_by}"]
    
    print(f"\n{'='*50}")
    print(f"📊 REPORT: {report.upper()}")
    print(tabulate(table_data, headers=headers, tablefmt="rounded_grid", 
                   showindex=range(1, len(table_data)+1)))
    print("🥳 REPORT READY")
    print(f"{'='*50}")


def main():
    parsed_args = parse_args()
    calc_by = column_select(parsed_args.files)
    gdp_by_country = read_from_csv(parsed_args.files, calc_by)
    
    if not gdp_by_country:
        print("🔴 Нет данных для обработки")
        return
    
    table = mean_gdp_calculate(gdp_by_country)
    draw_table(table, calc_by, parsed_args.report)

if __name__ == "__main__":
    main()
