from os.path import isfile  # , isdir, makedirs

from sqlalchemy import create_engine

from models import (
    metadata_obj,
    Nir_Grant,
    Nir_NTP,
    Nir_Templan,
    Nir_VUZ,
    NTP,
    Grant,
    Templan,
    VUZ,
    Pivot,
    create_table,
    create_pivot,
)


def create_sql_tables():
    # if not (isdir('DB')):
    #     makedirs('DB')
    if not (isfile("DB/DataBase.sqlite")):
        engine = create_engine("sqlite:///DB/DataBase.sqlite", echo=False)
        metadata_obj.drop_all(engine)
        metadata_obj.create_all(engine)
        create_table(Nir_Grant, Grant)
        create_table(Nir_NTP, NTP)
        create_table(Nir_Templan, Templan)
        create_table(Nir_VUZ, VUZ)
        create_pivot(Grant, NTP, Templan, Pivot)
