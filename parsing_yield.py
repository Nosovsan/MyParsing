# -*- coding: utf-8 -*-
import datetime
from bs4 import BeautifulSoup
import re
import json
import csv

# html = 'C:\\Users\\San\\Desktop\\Logbook.html'
# Открываем файл в рабочей директории
HTML = 'Logbook.html'
CSV = f"{HTML}_{datetime.date.today()}.csv"
COLS = ['Номер', 'Дата и время', 'Глюкоза', 'Углеводы', 'Кор. инсулин', 'Дл. инсулин', 'Медик', 'Категория',
        'Примечания', 'Дополнительно', 'Место укола'
        ]

"""
Получение данных измерений (объекты BeautifulSoup) из файла-экспорта
"""


def get_data():
    # try:
    record_items = []
    with open(HTML) as fp:
        soup = BeautifulSoup(fp, 'lxml')
    all_rec = soup.tbody.find_all("td", {"class": re.compile("table_row_col[1-9]+")})
    for rec in all_rec:
        yield rec
        record_items.append(rec)
    # except Exception as e:
    #     print("Exchange %s  %s  %s", e.__str__(), '[' + type(e).__name__ + ']', str(e)[0:200])
    #     print(f"Error open {HTML} file")
    # finally:
    # return record_items


def add_in_csv_caption(caption, file):
    try:
        with open(file, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp)
    except:
        print(f"File {file} save error")
    pass


def add_in_csv_records(items, file):
    try:
        print(f'Заносим в файл запись {items[0]}')
        with open(file, "a", encoding="utf-8", newline="") as f_csv:  # , newline=''
            writer = csv.writer(f_csv)  # DictWriter(f_csv, fieldnames=COLS)
            try:
                for item in items:
                    writer.writerow(clean_data(item))
            except:
                print(f"File {file} save error")
    except:
        print(f"File {file} open error")


def get_clean_data():
    try:
        items = []
        for rec in get_data():
            items.extend([''.join(rec.get_text(strip=True).replace('\xa0', ' '))])
        print(items)
    except:
        print(f"Ошибка преобразования строки\n{rec}")
    # items.append(''.join(item.get_text(strip=True).replace('\xa0', ' ')))  # for item in items.find_all('td'))
    # add_in_csv_records(items, CSV)


def processing_records(soup):
    # items = soup.find_all("td", {"class": re.compile("table_row_col[0-9]+$")})
    rec_items = soup.tbody.find_all('tr', class_="table_row")
    return rec_items


if __name__ == "__main__":
    # items = ()
    # items = get_clean_data()
    get_clean_data()