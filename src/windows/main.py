from PyQt6 import QtSql
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
import logging

from src.windows.analytics import AnalyticsDialog
from src.windows.about import AboutDialog
from src.windows.export import ExportDialog
from ui.py.main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_actions()
        self.db = self.connect_database()  

        if self.db:
            self.setup_table_models()  

    def setup_actions(self):
        analytic_action = QAction("Аналитика", self)
        analytic_action.triggered.connect(self.open_analytics)
        self.ui.analytics.addAction(analytic_action)

        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.open_about)
        self.ui.about.addAction(about_action)

        export_action = QAction("Экспорт", self)
        export_action.triggered.connect(self.open_export)
        self.ui.export_2.addAction(export_action)

    def connect_database(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DB/DataBase.sqlite")

        if not db.open():
            logging.error("Не удалось подключиться к базе данных.")
            return False
        return db  

    def setup_table_models(self):
        self.table1 = self.create_table_model("vuz", self.ui.tableView)
        self.table2 = self.create_table_model("nir_grant", self.ui.tableView_2)
        self.table3 = self.create_table_model("nir_ntp", self.ui.tableView_3)
        self.table4 = self.create_table_model("nir_templan", self.ui.tableView_4)

    def create_table_model(self, table_name, table_view):
        model = QtSql.QSqlTableModel()
        model.setTable(table_name)
        model.select()
        table_view.setModel(model)
        return model

    def open_analytics(self):
        self.analytics_window = AnalyticsDialog()
        self.analytics_window.show()

    def open_about(self):
        self.about_window = AboutDialog()
        self.about_window.show()

    def open_export(self):
        self.export_window = ExportDialog()
        self.export_window.show()

    
