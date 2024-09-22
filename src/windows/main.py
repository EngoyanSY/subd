from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction

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

    def open_analytics(self):
        self.analitycs_window = AnalyticsDialog()
        self.analitycs_window.show()

    def open_about(self):
        self.about_window = AboutDialog()
        self.about_window.show()

    def open_export(self):
        self.export_window = ExportDialog()
        self.export_window.show()
