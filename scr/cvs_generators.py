import csv
import datetime as dt
from pathlib import Path

from bs4 import PageElement

DT_FORMAT = 'D%y.%m.%dT%H.%M.%S'
CVS_PATH = Path('.').parent.absolute() / 'csv'


def generate_urban_env_stat_csv(table: PageElement) -> Path:
    filepath = CVS_PATH / f'urban_env_stat_{dt.datetime.now().strftime(DT_FORMAT)}.csv'
    years = []
    for th in table.div.contents[1].table.thead.tr:
        years.append(th.span.text)
    regions = []
    for tr in table.contents[1].table.tbody:
        regions.append(tr.td.text)
    points = table.contents[2].div.div.div.table.tbody
    with filepath.open('a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['region', *years])
        for n, region in enumerate(regions):
            values = [td.text for td in points.contents[n]]
            writer.writerow([region, *values])
    return filepath

def generate_rel_urban_stat_csv(table: PageElement) -> Path:
    filepath = CVS_PATH / f'rel_urban_env_stat_{dt.datetime.now().strftime(DT_FORMAT)}.csv'
    colum_data = {}
    for n, th in enumerate(table.contents[0].contents[1].table.thead.contents[1]):
        colum_data[str(n)] = {
            'year': th['data-field-sort'][:4],
            'period': th.contents[1].text
            }
    data_rows = table.contents[2].div.div.div.table.tbody.contents
    csv_rows = []
    for n, tr in enumerate(table.contents[1].table.tbody):
        region = tr.td.text
        for td in data_rows[n]:
            col = td['data-col']
            data = [
                region,
                colum_data[col]['year'],
                colum_data[col]['period'],
                td.text
            ]
            csv_rows.append(data)
    with filepath.open('a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['region', 'year', 'period', 'value'])
        for row in csv_rows:
            writer.writerow(row)
    return filepath
