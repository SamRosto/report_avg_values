import pytest
import tempfile
import io
from unittest.mock import patch, MagicMock, call
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import (
    main,
    parse_args,
    get_available_columns,
    get_row,
    column_select,
    read_from_csv,
    mean_gdp_calculate,
    draw_table
)

# Тестовые CSV файлы
TEST_CSV1 = """country,gdp,population
USA,25000000,331000000
China,18000000,1440000000
"""

TEST_CSV2 = """Country,gdp,pop
USA,26000000,332000000
Australia,1543000,26000000
"""

@pytest.fixture
def temp_csv1(tmp_path):
    file_path = tmp_path / "test1.csv"
    file_path.write_text(TEST_CSV1)
    return str(file_path)

@pytest.fixture
def temp_csv2(tmp_path):
    file_path = tmp_path / "test2.csv"
    file_path.write_text(TEST_CSV2)
    return str(file_path)

def test_get_available_columns(temp_csv1):
    columns = get_available_columns(temp_csv1)
    assert columns == ['country', 'gdp', 'population']

def test_get_row_found():
    mock_reader = MagicMock()
    mock_reader.fieldnames = ['Country', 'GDP', 'pop']
    result = get_row(mock_reader, 'gdp')
    assert result == 'GDP'

def test_get_row_not_found():
    mock_reader = MagicMock()
    mock_reader.fieldnames = ['country', 'population']
    result = get_row(mock_reader, 'gdp')
    assert result is None

def test_read_from_csv_single_file(temp_csv1):
    data = read_from_csv([temp_csv1], 'gdp')
    assert 'USA' in data
    assert data['USA'] == ['25000000']
    assert 'China' in data
    assert data['China'] == ['18000000']

def test_read_from_csv_multiple_files(temp_csv1, temp_csv2):
    data = read_from_csv([temp_csv1, temp_csv2], 'gdp')
    assert 'USA' in data and len(data['USA']) == 2
    assert set(data['USA']) == {'25000000', '26000000'}

def test_read_from_csv_missing_column(temp_csv1):
    """Тест ветки if row_key is None"""
    no_gdp_csv = """country,populationUSA,331000000"""
    no_gdp_path = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
    no_gdp_path.write(no_gdp_csv.encode())
    no_gdp_path.close()
    
def test_read_from_csv_country_variants(temp_csv1):
    """Тест row.get('country', row.get('Country'))"""
    data = read_from_csv([temp_csv1], 'population')
    assert 'USA' in data
    assert data['USA'] == ['331000000']

def test_mean_gdp_calculate():
    #test mean_gdp_calculate
    data = {'USA': ['25000000', '26000000'], 'China': ['18000000']}
    result = mean_gdp_calculate(data)
    assert result['USA'] == 25500000.0
    assert result['China'] == 18000000.0

def test_mean_gdp_calculate_empty_list():
    """Тест if v"""
    data = {'USA': []}
    result = mean_gdp_calculate(data)
    assert result == {}

def test_draw_table(capsys):
    # test draw_table
    table = {'USA': 25500000.0, 'China': 18000000.0}
    draw_table(table, 'gdp', 'test-report')
    captured = capsys.readouterr()
    assert "REPORT: TEST-REPORT" in captured.out
    assert "USA" in captured.out

@pytest.mark.parametrize("user_inputs,expected", [
    # test column_select
    (["gdp"], "gdp"),
    (["population"], "population"),
    (["country"], None),  
    (["gdo", "gdp"], "gdp"),
])
def test_column_select(mocker, tmp_path, user_inputs, expected):
    temp_file = tmp_path / "test.csv"
    temp_file.write_text(TEST_CSV1)
    
    mocker.patch('builtins.input', side_effect=user_inputs)
    mocker.patch('main.get_available_columns', 
                return_value=['country', 'gdp', 'population'])
    
    if expected:
        result = column_select([str(temp_file)])
        assert result == expected
    else:
        with pytest.raises(StopIteration):  # Бесконечный цикл прервётся
            column_select([str(temp_file)])
