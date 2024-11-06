from PyQt6 import QtSql
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from src.windows.about import AboutDialog
from src.windows.export import ExportDialog
from ui.py.main_window import Ui_MainWindow
from models import VUZ
from core import Session
from src.components.vuz_table_models import VuzTableModel
from src.components.grant_table_models import GrantTableModel
from src.components.ntp_table_models import NTPTableModel
from src.components.templan_table_models import TemplanTableModel
from src.components.pivot_table_models import PivotTableModel
from src.components.grnti_table_models import GRNTITableModel


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

    def setup_actions(self):
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.open_about)
        self.ui.about.addAction(about_action)

        self.ui.action_5.triggered.connect(self.open_export)
        self.ui.action_6.triggered.connect(self.open_export)
        self.ui.action_7.triggered.connect(self.open_export)
        self.ui.action_8.triggered.connect(self.open_export)

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
        grnti_code = self.ui.grnti_code.text()
        if grnti_code:
            self.filter_cond["grnti_code"] = grnti_code
        self.setupFilters(self.filter_cond)

    def clear_filters(self):
        self.filter_cond = {}
        self.setupFilters(self.filter_cond)

    def setup_table_models(self):
        self.table_vuz = VuzTableModel()
        self.ui.tableView.setModel(self.table_vuz)
        self.ui.tableView.setEditTriggers(self.ui.tableView.EditTrigger.NoEditTriggers)
        self.ui.tableView.resizeColumnsToContents()

        self.table_grant = GrantTableModel()
        self.ui.tableView_2.setModel(self.table_grant)
        self.ui.tableView_2.setEditTriggers(self.ui.tableView_2.EditTrigger.NoEditTriggers)
        self.ui.tableView_2.resizeColumnsToContents()

        self.table_ntp = NTPTableModel()
        self.ui.tableView_3.setModel(self.table_ntp)
        self.ui.tableView_3.setEditTriggers(self.ui.tableView_3.EditTrigger.NoEditTriggers)
        self.ui.tableView_3.resizeColumnsToContents()

        self.table_templan = TemplanTableModel()
        self.ui.tableView_4.setModel(self.table_templan)
        self.ui.tableView_4.setEditTriggers(self.ui.tableView_4.EditTrigger.NoEditTriggers)
        self.ui.tableView_4.resizeColumnsToContents()

        self.pivot = PivotTableModel()
        self.ui.tableView_13.setModel(self.pivot)
        self.ui.tableView_13.setEditTriggers(self.ui.tableView_13.EditTrigger.NoEditTriggers)    
        self.ui.tableView_13.resizeColumnsToContents()

        self.grnti = GRNTITableModel()
        self.ui.tableView_14.setModel(self.grnti)
        self.ui.tableView_14.setEditTriggers(self.ui.tableView_14.EditTrigger.NoEditTriggers)    
        self.ui.tableView_14.resizeColumnsToContents()

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
                "name": sorted(list(set([v[0] for v in vuz]))),
                "city": sorted(list(set([v[1] for v in vuz]))),
                "region": sorted(list(set([v[2] for v in vuz]))),
                "federation_subject": sorted(list(set([v[3] for v in vuz]))),
            }
        self.ui.vuz.clear()
        self.ui.vuz.addItems(vuz["name"])
        self.ui.city.clear()
        self.ui.city.addItems(vuz["city"])
        self.ui.obl.clear()
        self.ui.obl.addItems(vuz["region"])
        self.ui.subject.clear()
        self.ui.subject.addItems(vuz["federation_subject"])
        filter_2 = {}
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
            filter_2 = {"vuz_name": vuz["name"]}
            filter_3 = filter_2.copy()
            if "grnti_code" in filters_vuz:
                filter_2["grnti_code"] = filters_vuz["grnti_code"]
                del filters_vuz["grnti_code"]
        self.ui.tableView.model().setFilter(filters_vuz)
        self.ui.tableView_13.model().setFilter(filter_3)
        self.ui.tableView_2.model().setFilter(filter_2)
        self.ui.tableView_3.model().setFilter(filter_2)
        self.ui.tableView_4.model().setFilter(filter_2)

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
