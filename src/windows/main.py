from PyQt6 import QtSql
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from src.windows.about import AboutDialog
from src.windows.export import ExportDialog
from ui.py.main_window import Ui_MainWindow
from src.align_delegate import AlignDelegate
from models import VUZ, Grant, NTP, Templan, Pivot, BaseTable
from core import Session


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()
        self.db = self.connect_database()

        if self.db:
            self.setup_table_models()

        self.setWindowTitle("Анализ сводных показателей выполнения НИР - Вариант 10")
        self.showMaximized()

        self.setup_sorting()
        self.filter_cond = {}
        self.setupFilters()

    @property
    def vuz_column_names(self):
        return {
            "vuz_code": "Код",
            "name": "Наименование",
            "full_name": "Полное наименование",
            "vuz_name": "Аббревиатура",
            "region": "Регион",
            "city": "Город",
            "status": "Статус",
            "fed_sub_code": "Код фед. субъекта",
            "federation_subject": "Фед. субъект",
            "gr_ved": "ГР ВЭД",
            "profile": "Профиль",
        }

    @property
    def nir_grant_column_names(self):
        return {
            "nir_code": "Код НИР",
            "kon_code": "Код конкурса",
            "vuz_code": "Код ВУЗа",
            "vuz_name": "Наименование ВУЗа",
            "grnti_code": "Код по ГРНТИ",
            "grant_value": "Пл. объём гранта",
            "nir_name": "Наименование НИР",
            "nir_director": "Руководитель НИР",
            "director_position": "Должность",
            "director_academic_title": "Ученое звание",
            "director_academic_degree": "Ученая степень",
        }

    @property
    def nir_ntp_column_names(self):
        return {
            "ntp_code": "Код НТП",
            "nir_number": "Номер НИР",
            "nir_name": "Наименование НИР",
            "vuz_code": "Код ВУЗа",
            "vuz_name": "Наименование ВУЗа",
            "nir_organization": "Организация-исполнитель НИР",
            "nir_org_code": "Код организации-исполнителя НИР",
            "nir_director": "Руководитель НИР",
            "director_meta": "Должность, Уч. звание, Уч. степень",
            "grnti_code": "Код ГРНТИ НИР",
            "nir_type": "Характер НИР",
            "year_value_plan": "Пл. фин-е текущего года",
        }

    @property
    def nir_templan_column_names(self):
        return {
            "vuz_name": "Наименование ВУЗа",
            "vuz_code": "Код ВУЗа",
            "nir_type": "Характер НИР",
            "vuz_abb": "Аббревиатура ВУЗа",
            "nir_director": "Руководитель НИР",
            "grnti_theme_code": "Код ГРНТИ НИР",
            "value_plan": "Пл. финансирование",
            "nir_name": "Наименование НИР",
            "director_position": "Должность",
            "nir_reg_number": "Номер НИР",
            "grnti_code": "Код ГРНТИ НИР",
        }

    @property
    def pivot_column_names(self):
        return {
            "vuz_code": "Код ВУЗа",
            "vuz_name": "Наименование ВУЗа",
            "total_nir_grant_count": "Кол-во по грантам",
            "total_grant_value": "Сумма по грантам",
            "total_nir_ntp_count": "Кол-во по НТП",
            "total_year_value_plan": "Сумма по НТП",
            "total_value_plan": "Сумма по тем. планам",
            "total_nir_templan_count": "Кол-во по тем. планам",
            "total_count": "Общее кол-во",
            "total_sum": "Общая сумма",
        }

    def setup_actions(self):
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.open_about)
        self.ui.about.addAction(about_action)

        export_action = QAction("Экспорт", self)
        export_action.triggered.connect(self.open_export)
        self.ui.export_2.addAction(export_action)

        self.ui.set_filter.clicked.connect(self.set_filters)
        self.ui.clear_filter.clicked.connect(self.clear_filters)

    def connect_database(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DB/DataBase.sqlite")

        if not db.open():
            raise Exception("Не удалось подключиться к базе данных.")

        return db

    def set_filters(self):
        vuz_name = self.ui.vuz.currentText()
        if self.ui.vuz.currentIndex() != -1:
            self.filter_cond["vuz_name"] = vuz_name
        vuz_city = self.ui.city.currentText()
        if self.ui.city.currentIndex() != -1:
            self.filter_cond["city"] = vuz_city
        vuz_fed_sub = self.ui.subject.currentText()
        if self.ui.subject.currentIndex() != -1:
            self.filter_cond["federation_subject"] = vuz_fed_sub
        vuz_region = self.ui.obl.currentText()
        if self.ui.obl.currentIndex() != -1:
            self.filter_cond["region"] = vuz_region
        grnti_code = self.ui.grnti_code.currentText()
        if self.ui.grnti_code.currentIndex() != -1:
            self.filter_cond["grnti_code"] = grnti_code
        self.setupFilters(self.filter_cond)

    def clear_filters(self):
        self.filter_cond = {}
        self.setupFilters(self.filter_cond)

    def get_column_names(self, table_name):
        table_column_properties = {
            "vuz": self.vuz_column_names,
            "nir_grant": self.nir_grant_column_names,
            "nir_ntp": self.nir_ntp_column_names,
            "nir_templan": self.nir_templan_column_names,
            "pivot": self.pivot_column_names,
        }

        return table_column_properties.get(table_name, {})

    def rename_table_columns(self, table_name, qt_table):
        column_names = self.get_column_names(table_name)

        for old_name, new_name in column_names.items():
            col_index = qt_table.fieldIndex(old_name)
            if col_index != -1:
                qt_table.setHeaderData(col_index, Qt.Orientation.Horizontal, new_name)

    def setup_table_models(self):
        self.table_vuz = self.create_table_model(VUZ, self.ui.tableView)
        self.table_grant = self.create_table_model(Grant, self.ui.tableView_2)
        self.table_ntp = self.create_table_model(NTP, self.ui.tableView_3)
        self.table_templan = self.create_table_model(Templan, self.ui.tableView_4)
        self.pivot = self.create_table_model(Pivot, self.ui.tableView_13)

    def create_table_model(self, table: BaseTable, table_view):
        qt_table = QtSql.QSqlTableModel()
        qt_table.setTable(table.__table__.name)
        qt_table.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnManualSubmit)
        qt_table.select()

        column_index = qt_table.fieldIndex("UniqueID")

        header = table_view.horizontalHeader()
        header.setSectionsClickable(True)
        header.setSortIndicatorShown(True)
        header.sectionClicked.connect(self.sort_table)

        if column_index != -1:
            qt_table.removeColumn(column_index)

        self.rename_table_columns(table.__table__.name, qt_table)

        delegate = AlignDelegate(table_name, table_view)
        table_view.setItemDelegate(delegate)

        table_view.setModel(qt_table)
        table_view.setEditTriggers(table_view.EditTrigger.NoEditTriggers)
        table_view.resizeColumnsToContents()
        return qt_table

    def setup_sorting(self):
        self.current_sort_column = None
        self.current_sort_order = Qt.SortOrder.DescendingOrder

    def setupFilters(self, filters_vuz={}):
        with Session() as session:
            vuz = (
                session.execute(VUZ().filter(filter_cond=filters_vuz))
                .columns("vuz_name", "city", "region", "federation_subject")
                .all()
            )
            vuz = {
                "name": set([v[0] for v in vuz]),
                "city": set([v[1] for v in vuz]),
                "region": set([v[2] for v in vuz]),
                "federation_subject": set([v[3] for v in vuz]),
            }
            grnti_codes = (
                session.execute(NTP().filter(filter_cond=filters_vuz))
                .columns("grnti_code")
                .all()
                + session.execute(Grant().filter(filter_cond=filters_vuz))
                .columns("grnti_code")
                .all()
                + session.execute(Templan().filter(filter_cond=filters_vuz))
                .columns("grnti_code")
                .all()
            )

        grnti_codes_clean = set()
        for code in map(lambda x: x[0], grnti_codes):
            if code and code != "???":
                splitter = ""
                if ":" in code:
                    splitter = ":"
                elif "," in code:
                    splitter = ","
                elif ";" in code:
                    splitter = ";"
                elif " " in code:
                    splitter = " "
                if splitter:
                    a, b = code.split(splitter)
                    grnti_codes_clean.add(a.strip())
                    grnti_codes_clean.add(b.strip())
                else:
                    grnti_codes_clean.add(code.strip())
        grnti_codes_clean = list(
            set(map(lambda x: x[: min(5, len(x))], grnti_codes_clean))
        )
        self.ui.vuz.clear()
        self.ui.vuz.addItems(vuz["name"])
        self.ui.city.clear()
        self.ui.city.addItems(vuz["city"])
        self.ui.obl.clear()
        self.ui.obl.addItems(vuz["region"])
        self.ui.subject.clear()
        self.ui.subject.addItems(vuz["federation_subject"])
        self.ui.grnti_code.clear()
        self.ui.grnti_code.addItems(sorted(list(grnti_codes_clean)))
        filter_1, filter_2 = "", ""
        if filters_vuz is not None:
            self.ui.vuz.setCurrentText(
                filters_vuz["vuz_name"] if "vuz_name" in filters_vuz else "ВУЗ"
            )
            self.ui.city.setCurrentText(
                filters_vuz["city"] if "city" in filters_vuz else "Город"
            )
            self.ui.obl.setCurrentText(
                filters_vuz["region"] if "region" in filters_vuz else "Регион"
            )
            self.ui.subject.setCurrentText(
                filters_vuz["federation_subject"]
                if "federation_subject" in filters_vuz
                else "Субъект Федерации"
            )
            self.ui.grnti_code.setCurrentText(
                filters_vuz["grnti_code"]
                if "grnti_code" in filters_vuz
                else "Код ГРНТИ"
            )
            filter_1 = " AND ".join(
                list(map(lambda x: f"{x[0]} LIKE '{x[1]}'", filters_vuz.items()))
            )
            filter_2 = " OR ".join(list(map(lambda x: f"vuz_name='{x}'", vuz["name"])))
            if "grnti_code" in filters_vuz:
                filter_2 = (
                    f"({filter_2}) AND grnti_code LIKE '{filters_vuz['grnti_code']}%'"
                )

        self.ui.tableView.model().setFilter(filter_1)
        self.ui.tableView.model().select()
        self.ui.tableView_13.model().setFilter(filter_2)
        self.ui.tableView_13.model().select()
        self.ui.tableView_2.model().setFilter(filter_2)
        self.ui.tableView_2.model().select()
        self.ui.tableView_3.model().setFilter(filter_2)
        self.ui.tableView_3.model().select()
        self.ui.tableView_4.model().setFilter(filter_2)
        self.ui.tableView_4.model().select()

    def sort_table(self, index):
        table_view = self.sender().parent()
        model = table_view.model()

        if self.current_sort_column == index:
            self.current_sort_order = (
                Qt.SortOrder.DescendingOrder
                if self.current_sort_order == Qt.SortOrder.AscendingOrder
                else Qt.SortOrder.AscendingOrder
            )
        else:
            self.current_sort_column = index
            self.current_sort_order = Qt.SortOrder.DescendingOrder

        model.sort(self.current_sort_column, self.current_sort_order)

    def open_about(self):
        self.about_window = AboutDialog()
        self.about_window.show()

    def open_export(self):
        self.export_window = ExportDialog()
        self.export_window.show()
