from datetime import datetime

from django.utils.dateparse import parse_datetime

import petl
from petl.io.json import DictsView


def convert_datetime_to_date(iso_timestamp: str):
    dt = parse_datetime(iso_timestamp)
    return datetime.strftime(dt, "%Y-%m-%d")


def transform_people(people: list) -> DictsView:
    fields = [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "date",
    ]

    table = petl.fromdicts(people)
    table = petl.rename(table, "created", "date")
    table = petl.cut(table, *fields)
    table = petl.convert(
        table, {"date": convert_datetime_to_date, "homeworld": lambda rec: rec["name"]}
    )
    return table
