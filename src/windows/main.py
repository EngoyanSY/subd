from PyQt6 import QtSql
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt

from src.windows.about import AboutDialog
from src.windows.export import ExportDialog
from ui.py.main_window import Ui_MainWindow
from ..alignDelegate import AlignDelegate


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
            "fed_sub_code": "Код федерального субъекта",
            "federation_subject": "Федеральный субъект",
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
            "grant_value": "Плановый объём гранта",
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
            "year_value_plan": "Плановое финансирование текущего года",
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
            "value_plan": "Плановое финансирование",
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

    def connect_database(self):
        db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DB/DataBase.sqlite")

        if not db.open():
            raise Exception("Не удалось подключиться к базе данных.")

        return db

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
        self.table_vuz = self.create_table_model("vuz", self.ui.tableView)
        self.table_grant = self.create_table_model("nir_grant", self.ui.tableView_2)
        self.table_ntp = self.create_table_model("nir_ntp", self.ui.tableView_3)
        self.table_templan = self.create_table_model(
            "nir_templan", self.ui.tableView_4
        )
        self.pivot = self.create_table_model("pivot", self.ui.tableView_13)

    def create_table_model(self, table_name, table_view):
        qt_table = QtSql.QSqlTableModel()
        qt_table.setTable(table_name)
        qt_table.setEditStrategy(QtSql.QSqlTableModel.EditStrategy.OnManualSubmit)
        qt_table.select()

        column_index = qt_table.fieldIndex("UniqueID")
        
        header = table_view.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.sort_table)

        if column_index != -1:
            qt_table.removeColumn(column_index)

        self.rename_table_columns(table_name, qt_table)

        delegate = AlignDelegate(table_view)
        table_view.setItemDelegate(delegate)

        table_view.setModel(qt_table)
        table_view.setEditTriggers(table_view.EditTrigger.NoEditTriggers)
        table_view.resizeColumnsToContents()
        return qt_table

    def setup_sorting(self):
        self.current_sort_column = None
        self.current_sort_order = Qt.SortOrder.DescendingOrder


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
