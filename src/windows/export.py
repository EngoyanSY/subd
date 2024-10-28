from PyQt6.QtWidgets import QDialog, QMessageBox
from ui.py.export_window import Ui_Dialog

from docx import Document
from docx.shared import Pt, Inches
from core import Session
from models import Pivot


class ExportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Экспорт отчётов")
        # Подключаем сигнал кнопки Ok для вызова функции create_report
        self.ui.pushButton_save.clicked.connect(self.create_report)
        self.ui.pushButton_cancel.clicked.connect(self.close)

    def create_report(self):
        make_report()  # Вызов функции make_report, которая определена ниже
        self.show_notification(
            "Отчёт успешно сохранён в папку DB!"
        )  # Показываем уведомление

    def show_notification(self, message):
        # Создаём всплывающее сообщение
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Уведомление")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Устанавливаем фиксированную высоту
        msg_box.setFixedHeight(500)  # Установите нужную высоту

        msg_box.exec()  # Показываем сообщение пользователю


def make_report():
    with Session() as session:
        rows = session.query(Pivot).all()

        doc = Document()
        doc.add_heading("Отчет из совдной таблицы", level=1)
        table = doc.add_table(rows=1, cols=len(Pivot.__table__.columns))

        # Настройка полей страницы
        section = doc.sections[0]
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

        # Заголовки столбцов
        column_names = [
            "Ном",
            "Код",
            "ВУЗ",
            "Кол-во гр",
            "Сумма гр",
            "Кол-во НТП",
            "Сумма НТП",
            "Сумма тп",
            "Кол-во тп",
            "Общее кол-во",
            "Общая сумма",
        ]

        hdr_cells = table.rows[0].cells
        for i, column in enumerate(column_names):
            hdr_cells[i].text = column
            for paragraph in hdr_cells[i].paragraphs:
                run = paragraph.runs[0]
                run.font.name = "Times New Roman"
                run.font.size = Pt(10)  # размер шрифта 10
            paragraph.paragraph_format.space_after = 0

        for row in rows:
            row_cells = table.add_row().cells
            row_cells[0].text = str(row.UniqueID)
            row_cells[1].text = str(row.vuz_code)
            row_cells[2].text = str(row.vuz_name)
            row_cells[3].text = str(row.total_nir_grant_count)
            row_cells[4].text = str(row.total_grant_value)
            row_cells[5].text = str(row.total_nir_ntp_count)
            row_cells[6].text = str(row.total_year_value_plan)
            row_cells[7].text = str(row.total_nir_templan_count)
            row_cells[8].text = str(row.total_value_plan)
            row_cells[9].text = str(row.total_count)
            row_cells[10].text = str(row.total_sum)

            # Установка шрифта для ячеек с данными
            for cell in row_cells:
                for paragraph in cell.paragraphs:
                    run = paragraph.runs[0]
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(10)

        table.style = "Table Grid"
        set_table_width(table)

        doc.save("DB/Сводная таблица.docx")

    print("Отчет успешно создан и сохранен как report.docx.")


def set_table_width(table):
    for row in table.rows:
        for cell in row.cells:
            # Устанавливаем ширину ячейки равной её контенту
            cell.width = Pt(0)  # Автоматически подстраивает по контенту
            # Убираем обтекание текста
            cell.paragraphs[0].paragraph_format.space_after = 0
