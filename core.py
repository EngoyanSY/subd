from os.path import isfile

from sqlalchemy import create_engine

from models import (
    metadata_obj,
    NTP,
    Grant,
    Templan,
    VUZ,
    Pivot,
    create_table,
    create_pivot,
)

from schema import (
    Nir_Grant,
    Nir_NTP,
    Nir_Templan,
    Nir_VUZ,
)


def create_sql_tables():
    if not (isfile("DB/DataBase.sqlite")):
        engine = create_engine("sqlite:///DB/DataBase.sqlite", echo=False)
        metadata_obj.drop_all(engine)
        metadata_obj.create_all(engine)
        create_table(Nir_Grant, Grant)
        create_table(Nir_NTP, NTP)
        create_table(Nir_Templan, Templan)
        create_table(Nir_VUZ, VUZ)
        create_pivot(Grant, NTP, Templan, Pivot)
        print('База данных DataBase.sqlite создана и подключена')
    else:
        print('База данных DataBase.sqlite подключена')
