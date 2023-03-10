# -*- coding: utf-8 -*-
import datetime
import bs4
from bs4 import BeautifulSoup
import re
import csv

HTML_EXP = "Export_Diabets-M.html"  # Открываем файл в рабочей директории
CSV = f"RESULT\\{HTML_EXP}_{datetime.date.today()}.csv"
COLS = ['Номер', 'Дата и время', 'Глюкоза', 'Углеводы', 'Кор. инсулин', 'Дл. инсулин', 'Медик', 'Категория',
        'Примечания', 'Дополнительно', 'Место укола'
        ]


def get_data(html: str) -> bs4.element.ResultSet:
    """ Получение данных измерений (объекты BeautifulSoup) из файла-экспорта """
    with open(html) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    # all_rows = soup.find_all("td", {"class": re.compile('table_row_col[1-9]+')})
    return soup.find_all("td", {"class": re.compile('table_row_col[1-9]+')})
    # return all_rows


def clean_data_row(current_row: bs4.element.Tag) -> str:
    """ Чистим записи от ненужных символов """
    try:
        return current_row.get_text(strip=True).replace('\xa0', ' ') if len(current_row) else ""
    except Exception as ex:
        print(ex)
        print(f"Ошибка преобразования строки")


def list_row(all_rows: bs4.element.ResultSet) -> list[str]:
    """ Преобразование среза списка строк в блоки строк
    пример перебора срезов списка взят из интернета
        for i in range(len(items) // 500):
            _tmp = items[500 * i:500 * (i + 1)]
    """
    # r = []
    for i in range(len(all_rows) // 11):
        # r = [clean_data_row(item) for item in all_rows[11 * i: 11 * (i + 1)]]
        yield [clean_data_row(item) for item in all_rows[11 * i: 11 * (i + 1)]]
    # return r
    #     yield r


def write_records_to_csv_file(items: bs4.element.ResultSet, file: str):
    try:
        # with open(file, "w", encoding="utf-8", newline="") as file_csv:  # , newline='' "utf-8"
        with open(file, "w", encoding="cp1251", newline="", errors="ignore") as file_csv:  # , newline='' "utf-8"
            try:
                csv.writer(file_csv).writerow(COLS)
                csv.writer(file_csv).writerows(list_row(items))
            except Exception as ex:
                print(ex.args)
                print(f"File {file} save error")
    except Exception as ex:
        print(ex.args)
        print(f"File {file} open error")


if __name__ == "__main__":
    rows = get_data(HTML_EXP)
    write_records_to_csv_file(rows, CSV)
    print(f"Файл {CSV} загружен")
