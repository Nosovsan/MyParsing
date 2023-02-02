# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import re
import json
import csv

HTML_EXP = "Export_Diabets-M.html"  # Открываем файл в рабочей директории
CSV = f"RESULT\\{HTML_EXP}_{datetime.date.today()}.csv"
COLS = ['Номер', 'Дата и время', 'Глюкоза', 'Углеводы', 'Кор. инсулин', 'Дл. инсулин', 'Медик', 'Категория',
        'Примечания', 'Дополнительно', 'Место укола'
        ]

def get_data(html: str) -> set:
    """ Получение данных измерений (объекты BeautifulSoup) из файла-экспорта """
    with open(html) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    all_rows = soup.find_all("td", {"class": re.compile('table_row_col[1-9]+')})
    return all_rows


def clean_data_row(current_row: list) -> str:
    """ Чистим записи от ненужных символов """
    try:
        return current_row.get_text(strip=True).replace('\xa0', ' ') if len(current_row) else ""
    except Exception as ex:
        print(ex)
        print(f"Ошибка преобразования строки")


def list_row(all_rows: list) -> list[list[str]]:
    """ Преобразование среза списка строк в блоки строк
    пример перебора срезов списка взят из интернета
        for i in range(len(items) // 500):
            _tmp = items[500 * i:500 * (i + 1)]
    """
    r = []
    for i in range(len(all_rows) // 11):
        r.append([clean_data_row(item) for item in all_rows[11 * i: 11 * (i + 1)]])
    return r


def write_records_to_csv_file(items: list, file: str):
    try:
        print(f'Заносим в файл запись {items[0]}')
        with open(file, "w", encoding="utf-8", newline="") as file_csv:  # , newline='' "utf-8"
            try:
                writer = csv.writer(file_csv).writerow(COLS)
                writer = csv.writer(file_csv).writerows(items)
            except Exception as ex:
                print(ex.args)
                print(f"File {file} save error")
    except Exception as ex:
        print(ex.args)
        print(f"File {file} open error")


if __name__ == "__main__":
    rows = get_data(HTML_EXP)
    clean_rows = list_row(rows)
    write_records_to_csv_file(clean_rows, CSV)
    print(f"Файл {CSV} загружен")
