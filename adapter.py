import os
import sqlite3

import pandas as pd


class con_excel:
    DB = None

    def __init__(self, name):
        self.DB = pd.read_excel(os.path.join("DB", name))

    def print_head(self):
        return print(self.DB.head())

    def print_db(self):
        return print(self.DB)


class db_sql(con_excel):
    columns_name = None
    database_name = None

    def __init__(self, name):
        super(db_sql, self).__init__(name)
        self.DB = self.DB.rename(columns=dict(zip(self.DB.columns, self.columns_name)))

    def create_table(self):
        con = sqlite3.connect(os.path.join("DB", "DataBase.sqlite"))
        self.DB.to_sql(self.database_name, con, if_exists="replace", index=False)


class db_VUZ(db_sql):
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

    def __init__(self, name):
        super(db_VUZ, self).__init__(name)


class db_NTP(db_sql):
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

    def __init__(self, name):
        super(db_NTP, self).__init__(name)


class db_Gr(db_sql):
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

    def __init__(self, name):
        super(db_Gr, self).__init__(name)


class db_Tp(db_sql):
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

    def __init__(self, name):
        super(db_Tp, self).__init__(name)


def create_database():
    VUZ = db_VUZ("Vuz.xlsx")
    NTP = db_NTP("Ntp_pr.xlsx")
    GR = db_Gr("Gr_pr.xlsx")
    TP = db_Tp("Tp_pr.xlsx")

    VUZ.create_table()
    NTP.create_table()
    GR.create_table()
    TP.create_table()
