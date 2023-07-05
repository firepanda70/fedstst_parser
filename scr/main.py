from .parsers import load_urban_env_stat, load_rel_urban_stat
from .cvs_generators import generate_urban_env_stat_csv, generate_rel_urban_stat_csv
from .db_fillers import fill_urban_scores_db, fill_rel_urban_scores_db


def main():
    urban_table = load_urban_env_stat()
    urban_csv_file = generate_urban_env_stat_csv(urban_table)
    fill_urban_scores_db(urban_csv_file)

    rel_urban_table = load_rel_urban_stat()
    rel_urban_csv_file = generate_rel_urban_stat_csv(rel_urban_table)
    fill_rel_urban_scores_db(rel_urban_csv_file)
