from PyQt6.QtWidgets import QDialog

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
        self.setWindowTitle("Создание отчёта")
        
        # Подключаем сигнал кнопки Ok для вызова функции create_report
        self.ui.buttonBox.accepted.connect(self.create_report)

    def create_report(self):
        make_report()  # Вызов функции make_report, которая определена ниже

def make_report():
    column_names = {
        "UniqueID": "Уник. идентификатор",
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

    with Session() as session:
        rows = session.query(Pivot).all()

        doc = Document()
        doc.add_heading('Отчет из совдной таблицы', level=1)
        table = doc.add_table(rows=1, cols=len(Pivot.__table__.columns))

        # Настройка полей страницы
        section = doc.sections[0]
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

        hdr_cells = table.rows[0].cells
        for i, (col_key, col_name) in enumerate(column_names.items()):
            hdr_cells[i].text = col_name
            for paragraph in hdr_cells[i].paragraphs:
                run = paragraph.runs[0]
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10)
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
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(10)

        table.style = 'Table Grid'
        set_table_width(table)

        doc.save('DB/report.docx')

    print("Отчет успешно создан и сохранен как report.docx.")

def set_table_width(table):
    for row in table.rows:
        for cell in row.cells:
            # Устанавливаем ширину ячейки равной её контенту
            cell.width = Pt(0)  # Автоматически подстраивает по контенту
            # Убираем обтекание текста
            cell.paragraphs[0].paragraph_format.space_after = 0