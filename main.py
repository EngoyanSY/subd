import sys

from PyQt6.QtWidgets import QApplication

from src.windows.main import MainWindow

from models import create_sql_tables

if __name__ == "__main__":

    create_sql_tables()

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    app.exec()
