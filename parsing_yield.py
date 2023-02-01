# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import re
import json
import csv

# html = 'C:\\Users\\San\\Desktop\\Export_Diabets-M.html'
# Открываем файл в рабочей директории
HTML_EXP = "Export_Diabets-M.html"
CSV = f"\\result\\{HTML_EXP}_{datetime.date.today()}.csv"
COLS = ['Номер', 'Дата и время', 'Глюкоза', 'Углеводы', 'Кор. инсулин', 'Дл. инсулин', 'Медик', 'Категория',
        'Примечания', 'Дополнительно', 'Место укола'
        ]

"""
Получение данных измерений (объекты BeautifulSoup) из файла-экспорта
"""


def get_data(html):
    all_row = []
    row = []
    with open(html) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    all_rows = soup.find_all("td", {"class": re.compile('table_row_col[1-9]+')})
    return all_rows


# Чистим записи от ненужных символов
def clean_data(current_row):
    try:
        r = (current_row.get_text(strip=True).replace('\xa0', ' '))
        return r
    except Exception as ex:
        print(ex)
        print(f"Ошибка преобразования строки")


def list_row(row_items):
    count = 0
    r = []
    """ Переделать цикл. Пропускает item при count=11"""
    for item in row_items:
        if count < 11:
            r.append(clean_data(item))
            count += 1
        else:
            count = 0
            print(r)


def add_in_csv_caption(caption, file):
    try:
        with open(file, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(caption)
    except:
        print(f"File {file} save error")
    pass


# items.append(''.join(item.get_text(strip=True).replace('\xa0', ' ')))  # for item in items.find_all('td'))
# add_in_csv_records(items, CSV)


def add_in_csv_records(items, file):
    try:
        print(f'Заносим в файл запись {items[0]}')
        with open(file, "a", encoding="utf-8", newline="") as f_csv:  # , newline='' "utf-8"
            writer = csv.writer(f_csv)  # DictWriter(f_csv, fieldnames=COLS)
            try:
                for item in items:
                    writer.writerow(clean_data(item))
            except:
                print(f"File {file} save error")
    except:
        print(f"File {file} open error")


def processing_records(soup):
    # items = soup.find_all("td", {"class": re.compile("table_row_col[0-9]+$")})
    rec_items = soup.tbody.find_all('tr', class_="table_row")
    return rec_items


if __name__ == "__main__":
    rows = get_data(HTML_EXP)
    list_row(rows)
