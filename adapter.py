import os
import sqlite3

import pandas as pd


class ConExcel:
    DB = None

    def __init__(self, name):
        self.DB = pd.read_excel(os.path.join("DB", name))

    def print_head(self):
        print(self.DB.head())

    def print_db(self):
        print(self.DB)


class TableSQL(ConExcel):
    columns_name = None
    database_name = None

    def __init__(self, name):
        super().__init__(name)
        self.DB = self.DB.rename(columns=dict(zip(self.DB.columns, self.columns_name)))

    def create_table(self):
        con = sqlite3.connect(os.path.join("DB", "DataBase.sqlite"))
        self.DB.to_sql(self.database_name, con, if_exists="replace", index=False)


class TableVUZ(TableSQL):
    columns_name = [
        "UniqueID",
        "code",
        "name",
        "full_name",
        "abb",
        "region",
        "city",
        "status",
        "fed_sub_code",
        "federation_subject",
        "gr_ved",
        "profile",
    ]

    database_name = "vuz"


class TableNTP(TableSQL):
    columns_name = [
        "UniqueID",
        "ntp_code",
        "nir_number",
        "nir_name",
        "nir_organization",
        "nir_org_code",
        "nir_director",
        "director_meta",
        "grnti_code",
        "nir_type",
        "year_value_plan",
    ]

    database_name = "nir_ntp"


class TableGr(TableSQL):
    columns_name = [
        "UniqueID",
        "nir_code",
        "kon_code",
        "vuz_code",
        "vuz_name",
        "grnti_code",
        "grant_value",
        "nir_name",
        "nir_director",
        "director_position",
        "director_academic_title",
        "director_academic_degree",
    ]

    database_name = "nir_grant"


class TableTp(TableSQL):
    columns_name = [
        "UniqueID",
        "vuz_code",
        "nir_type",
        "vuz_abb",
        "nir_director",
        "grnti_theme_code",
        "value_plan",
        "nir_name",
        "director_position",
        "nir_reg_number",
    ]

    database_name = "nir_templan"


def create_database():
    vuz = TableVUZ("Vuz.xlsx")
    ntp = TableNTP("Ntp_pr.xlsx")
    gr = TableGr("Gr_pr.xlsx")
    tp = TableTp("Tp_pr.xlsx")

    vuz.create_table()
    ntp.create_table()
    gr.create_table()
    tp.create_table()
