from os.path import isfile

from sqlalchemy import create_engine

from models import (
    metadata_obj,
    NTP,
    Grant,
    Templan,
    VUZ,
    Pivot,
    create_pivot,
)


def create_sql_tables():
    if not (isfile("DB/DataBase.sqlite")):
        engine = create_engine("sqlite:///DB/DataBase.sqlite", echo=False)
        metadata_obj.drop_all(engine)
        metadata_obj.create_all(engine)
        gr_table = Grant()
        ntp_table = NTP()
        tp_table = Templan()
        vuz_table = VUZ()
        pivot_table = Pivot()
        gr_table.create_table()
        ntp_table.create_table()
        tp_table.create_table()
        vuz_table.create_table()

        create_pivot(gr_table, ntp_table, tp_table, pivot_table)
        print("База данных DataBase.sqlite создана и подключена")
    else:
        print("База данных DataBase.sqlite подключена")
