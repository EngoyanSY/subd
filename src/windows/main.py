from PyQt6 import QtSql
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction, QDesktopServices
from PyQt6.QtCore import Qt, QUrl

from src.windows.export import (
    PivotExportDialog,
    StatusExportDialog,
    RegionExportDialog,
    GRNTIExportDialog,
    CharacterExportDialog,
    MostExportDialog,
)
from ui.py.main_window import Ui_MainWindow
from models import VUZ
from core import Session
from src.components.vuz_table_models import VuzTableModel
from src.components.grant_table_models import GrantTableModel
from src.components.ntp_table_models import NTPTableModel
from src.components.templan_table_models import TemplanTableModel
from src.components.pivot_table_models import PivotTableModel
from src.components.grnti_table_models import GRNTITableModel
from src.align_delegate import AlignDelegate


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.filter_cond = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()
        self.db = self.connect_database()

        if self.db:
            self.setup_table_models()

        self.setWindowTitle("Анализ сводных показателей выполнения НИР - Вариант 10")
        self.showMaximized()

        self.setup_sorting()

        self.setupFilters()

    def setup_actions(self):
        about_action = QAction("Документация", self)
        about_action.triggered.connect(self.open_documentation)
        self.ui.about.addAction(about_action)

        self.ui.action_5.triggered.connect(
            self.open_export_subclass(PivotExportDialog)
        )
        self.ui.action_6.triggered.connect(
            self.open_export_subclass(RegionExportDialog)
        )
        self.ui.action_7.triggered.connect(
            self.open_export_subclass(StatusExportDialog)
        )
        self.ui.action_8.triggered.connect(
            self.open_export_subclass(GRNTIExportDialog)
        )
        #TODO: CharacterExportDialog
        self.ui.action_3.triggered.connect(
            self.open_export_subclass(MostExportDialog)
            )

        self.ui.set_filter.clicked.connect(self.set_filters)
        self.ui.clear_filter.clicked.connect(self.clear_filters)

    def open_documentation(self):
        file_path = "Doc.pdf"
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

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
            print(self.filter_cond)
        self.setupFilters(self.filter_cond)

    def clear_filters(self):
        self.filter_cond = {}
        self.ui.grnti_code.clear()
        # ПОТОМКИ !!!! НЕ ПЫТАЙТЕСЬ ПОНЯТЬ БОГА
        # ПРИМИТЕ ЕГО В СЕБЕ И  СМИРИТЕСЬ
        # ИНОГДА ОБСТОЯТЕЛЬСТВА  ВЫШЕ НАС И ВЫШЕ КВАС
        # абоба
        self.setupFilters(self.filter_cond)

    def setup_table_models(self):
        # Создание моделей
        self.table_vuz = VuzTableModel()
        self.ui.tableView.setModel(self.table_vuz)
        self.ui.tableView.setEditTriggers(self.ui.tableView.EditTrigger.NoEditTriggers)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.horizontalHeader().sectionClicked.connect(self.sort_table)
        vuz_delegate = AlignDelegate(table_name="vuz")
        self.ui.tableView.setItemDelegate(vuz_delegate)

        self.table_grant = GrantTableModel()
        self.ui.tableView_2.setModel(self.table_grant)
        self.ui.tableView_2.setEditTriggers(
            self.ui.tableView_2.EditTrigger.NoEditTriggers
        )
        self.ui.tableView_2.resizeColumnsToContents()
        self.ui.tableView_2.horizontalHeader().sectionClicked.connect(self.sort_table)
        grant_delegate = AlignDelegate(table_name="grant")
        self.ui.tableView_2.setItemDelegate(grant_delegate)

        self.table_ntp = NTPTableModel()
        self.ui.tableView_3.setModel(self.table_ntp)
        self.ui.tableView_3.setEditTriggers(
            self.ui.tableView_3.EditTrigger.NoEditTriggers
        )
        self.ui.tableView_3.resizeColumnsToContents()
        self.ui.tableView_3.horizontalHeader().sectionClicked.connect(self.sort_table)
        ntp_delegate = AlignDelegate(table_name="ntp")
        self.ui.tableView_3.setItemDelegate(ntp_delegate)

        self.table_templan = TemplanTableModel()
        self.ui.tableView_4.setModel(self.table_templan)
        self.ui.tableView_4.setEditTriggers(
            self.ui.tableView_4.EditTrigger.NoEditTriggers
        )
        self.ui.tableView_4.resizeColumnsToContents()
        self.ui.tableView_4.horizontalHeader().sectionClicked.connect(self.sort_table)
        templan_delegate = AlignDelegate(table_name="templan")
        self.ui.tableView_4.setItemDelegate(templan_delegate)

        self.pivot = PivotTableModel()
        self.ui.tableView_13.setModel(self.pivot)
        self.ui.tableView_13.setEditTriggers(
            self.ui.tableView_13.EditTrigger.NoEditTriggers
        )
        self.ui.tableView_13.resizeColumnsToContents()
        self.ui.tableView_13.horizontalHeader().sectionClicked.connect(self.sort_table)
        pivot_delegate = AlignDelegate(table_name="pivot")
        self.ui.tableView_13.setItemDelegate(pivot_delegate)

        self.grnti = GRNTITableModel()
        self.ui.tableView_14.setModel(self.grnti)
        self.ui.tableView_14.setEditTriggers(
            self.ui.tableView_14.EditTrigger.NoEditTriggers
        )
        self.ui.tableView_14.resizeColumnsToContents()
        self.ui.tableView_14.horizontalHeader().sectionClicked.connect(self.sort_table)
        grnti_delegate = AlignDelegate(table_name="grnti")
        self.ui.tableView_14.setItemDelegate(grnti_delegate)

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
            filter_4 = filters_vuz.copy()
            if "grnti_code" in filters_vuz:
                filter_2["grnti_code"] = filters_vuz["grnti_code"]
                del filter_4["grnti_code"]

        self.ui.tableView.model().setFilter(filter_4)
        self.ui.tableView_13.model().setFilter(filter_3)
        self.ui.tableView_2.model().setFilter(filter_2)
        self.ui.tableView_3.model().setFilter(filter_2)
        self.ui.tableView_4.model().setFilter(filter_2)

    def setup_sorting(self):
        self.current_sort_column = None
        self.current_sort_order = Qt.SortOrder.DescendingOrder

    def sort_table(self, index):
        table_view = self.sender().parent()
        model = table_view.model()
        header = table_view.horizontalHeader()

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

        header.setSortIndicator(self.current_sort_column, self.current_sort_order)
        header.setSortIndicatorShown(True)

    def open_export_subclass(self, export_window_class):
        def open_export():
            self.export_window = export_window_class(self.filter_cond)
            self.export_window.show()

        return open_export
