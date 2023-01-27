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

def save_doc(s, file, mode = "w"):
    try:
        print(f'Заносим в файл запись {s[0]}')
        with open(file, mode=mode, encoding="utf-8", newline="") as f_csv:  # , newline=''
            writer = csv.writer(f_csv)  # DictWriter(f_csv, fieldnames=COLS)
            try:
                writer.writerow(s)
            except:
                print(f"File {file} save error")
    except:
        print(f"File {file} open error")


def clean_data(items):
    s = []
    for item in items:
        # s.append(''.join(item.get_text(strip=True).replace('\xa0', ' ')))  # for item in items.find_all('td'))
        s.append(''.join(item.get_text(strip=True).replace('\xa0', ' ')))  # for item in items.find_all('td'))
    # save_doc(s, CSV)
    return s

def get_content(html):
    with open(html) as fp:
        bsObj = BeautifulSoup(fp, 'lxml')
    return bsObj

def processing_records(soup):
    items = soup.find_all("td", str({"class"}).startswith("table_row_col"))
    # items = soup.find_all("td", {"class":re.compile("table_row_col[0-9]+$")})
    # items = soup.tbody.find_all('tr', class_="table_row")
    start = 0
    finish = 11
    range_records = 11

    item = items[start:finish]
    save_doc(COLS, CSV, "w")
    while len(item) > 0:
        save_doc(clean_data(item), CSV, "a")
        start += 11
        finish += 11
        item = items[start:finish]


if __name__ == "__main__":
    recods_data = []
    soup = get_content(HTML)
    records_list = processing_records(soup)
#     records = get_content(HTML)
#     save_doc(records, CSV)
