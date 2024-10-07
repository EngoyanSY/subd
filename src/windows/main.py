from PyQt6 import QtSql
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

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

        self.setWindowTitle("Анализ сводных показателей выполнения НИР - Вариант 10")
        self.showMaximized()

        self.setup_sorting()

    def setup_actions(self):
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
            raise Exception("Не удалось подключиться к базе данных.")

        return db

    def setup_table_models(self):
        self.table_vuz = self.create_table_model("vuz", self.ui.tableView)
        self.table_grant = self.create_table_model("nir_grant", self.ui.tableView_2)
        self.table_ntp = self.create_table_model("nir_ntp", self.ui.tableView_3)
        self.table_templan = self.create_table_model("nir_templan", self.ui.tableView_4)

        for table_view in [self.ui.tableView, self.ui.tableView_2, self.ui.tableView_3, self.ui.tableView_4]:
            table_view.resizeColumnsToContents()

    def create_table_model(self, table_name, table_view):
        model = QtSql.QSqlTableModel()
        model.setTable(table_name)
        model.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnManualSubmit)
        model.select()
        table_view.setModel(model)
        table_view.setEditTriggers(table_view.EditTrigger.NoEditTriggers)
        return model
    
    def setup_sorting(self):
        self.current_sort_column = None
        self.current_sort_order = Qt.SortOrder.DescendingOrder

        for table_view in [self.ui.tableView, self.ui.tableView_2, self.ui.tableView_3, self.ui.tableView_4]:
            header = table_view.horizontalHeader()
            header.setSectionsClickable(True)  
            header.sectionClicked.connect(self.sort_table)  

    def sort_table(self, index):
        table_view = self.sender().parent()
        model = table_view.model()

        if self.current_sort_column == index:
            self.current_sort_order = (
                Qt.SortOrder.DescendingOrder if self.current_sort_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
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
