import logging

from peewee import *

from .config import config


db = PostgresqlDatabase(
    config.db_name, user=config.db_user, password=config.db_pass,
    host=config.db_host, port=config.db_port
)

models_logger = logging.getLogger(__name__)
models_logger.setLevel(logging.INFO)

log_handler = logging.FileHandler(f"logs/{__name__}.log", mode='w', encoding='utf-8')
models_logger.addHandler(log_handler)


class Region(Model):
    name = CharField(unique=True)

    class Meta:
        database = db

    @classmethod
    def create(cls, **query):
        res = super().create(**query)
        models_logger.info(f'Created {res}')
        return res

    @classmethod
    def get_by_name(cls, name: str) -> 'Region':
        try:
            res = Region.select().where(Region.name == name).get()
            return res
        except DoesNotExist:
            return False
    
    def __str__(self) -> str:
        return f'Region {self.get_id()}'

class YearlyScore(Model):
    year = IntegerField()
    value = IntegerField(null=True)
    region = ForeignKeyField(Region, backref='scores')

    class Meta:
        database = db
        indexes = (
            (('year', 'region'), True),
        )

    @classmethod
    def create_or_update(cls, year: int, value: int, region: Region) -> 'YearlyScore':
        try:
            score: YearlyScore = YearlyScore.select().where(
                YearlyScore.year == year).where(
                YearlyScore.region == region
            ).get()
        except DoesNotExist:
            score = YearlyScore.create(year=year, value=value, region=region)
            models_logger.info(f'Created {score}')
            return score
        score.value = value
        score.save()
        models_logger.info(f'Updated {score}')
        return score
    
    def __str__(self) -> str:
        return f'YearlyScore {self.get_id()}'


class YearlyRelativeScore(Model):
    year = IntegerField()
    value = IntegerField(null=True)
    period = CharField()
    region = ForeignKeyField(Region, backref='rel_scores')

    @classmethod
    def create_or_update(cls, year: int, value: int, period: str, region: Region) -> 'YearlyRelativeScore':
        try:
            score: YearlyRelativeScore = YearlyRelativeScore.select().where(
                YearlyRelativeScore.year == year).where(
                YearlyRelativeScore.region == region).where(
                YearlyRelativeScore.period == period
                ).get()
        except DoesNotExist:
            score = YearlyRelativeScore.create(year=year, value=value, period=period, region=region)
            models_logger.info(f'Created {score}')
            return score
        score.value = value
        score.save()
        models_logger.info(f'Updated {score}')
        return score

    class Meta:
        database = db
        indexes = (
            (('year', 'region', 'period'), True),
        )

    def __str__(self) -> str:
        return f'YearlyRelativeScore {self.get_id()}'

def create_tables():
    with db:
        db.create_tables([Region, YearlyScore, YearlyRelativeScore])
