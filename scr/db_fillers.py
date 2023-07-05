import csv
from pathlib import Path

from .models import Region, YearlyScore, YearlyRelativeScore


def fill_urban_scores_db(csv_file: Path):
    with csv_file.open('r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['region']
            region = Region.get_by_name(name)
            if not region:
                region = Region.create(name=name)
            for year, value in [(key, value) for key, value in row.items() if key != 'region']:
                YearlyScore.create_or_update(year, value, region)


def fill_rel_urban_scores_db(csv_file: Path):
    with csv_file.open('r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        start = True
        for row in reader:
            if start:
                start = False
                continue
            name = row[0]
            region = Region.get_by_name(name)
            if not region:
                region = Region.create(name=name)
            year, period, value = row[1:]
            YearlyRelativeScore.create_or_update(year, value, period, region)
