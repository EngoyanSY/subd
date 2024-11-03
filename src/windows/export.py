from PyQt6.QtWidgets import (
    QDialog,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QComboBox,
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
)
from ui.py.export_window import Ui_Dialog

from docx import Document
from docx.shared import Pt, Inches
from core import Session
from models import Pivot
import os


class ExportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("Создание отчётов")
        self.resize(1280, 960)

        # Поле для ввода имени файла
        self.file_name_line_edit = QLineEdit(self)
        self.file_name_line_edit.setPlaceholderText("Введите имя файла")

        # Кнопка выбора пути для файла
        self.browse_button = QPushButton("Выбрать путь", self)
        self.browse_button.clicked.connect(self.browse_file)

        # Комбобоксы для фильтров
        self.filter_combobox_1 = QComboBox(self)
        self.filter_combobox_1.addItems(["Фильтр 1", "Фильтр 2", "Фильтр 3"])
        self.filter_combobox_1.setMinimumWidth(150)  # Укажите подходящую ширину
        self.filter_combobox_1.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.filter_combobox_1.currentIndexChanged.connect(self.update_preview)

        self.filter_combobox_2 = QComboBox(self)
        self.filter_combobox_2.addItems(["Фильтр 1", "Фильтр 2", "Фильтр 3"])
        self.filter_combobox_2.setMinimumWidth(150)  # Укажите подходящую ширину
        self.filter_combobox_2.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.filter_combobox_2.currentIndexChanged.connect(self.update_preview)

        self.filter_combobox_3 = QComboBox(self)
        self.filter_combobox_3.addItems(["Фильтр 1", "Фильтр 2", "Фильтр 3"])
        self.filter_combobox_3.setMinimumWidth(150)  # Укажите подходящую ширину
        self.filter_combobox_3.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.filter_combobox_3.currentIndexChanged.connect(self.update_preview)

        self.filter_combobox_4 = QComboBox(self)
        self.filter_combobox_4.addItems(["Фильтр 1", "Фильтр 2", "Фильтр 3"])
        self.filter_combobox_4.setMinimumWidth(150)  # Укажите подходящую ширину
        self.filter_combobox_4.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.filter_combobox_4.currentIndexChanged.connect(self.update_preview)

        self.filter_combobox_5 = QComboBox(self)
        self.filter_combobox_5.addItems(["Фильтр 1", "Фильтр 2", "Фильтр 3"])
        self.filter_combobox_5.setMinimumWidth(150)  # Укажите подходящую ширину
        self.filter_combobox_5.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.filter_combobox_5.currentIndexChanged.connect(self.update_preview)

        # Кнопки для установки и очистки фильтров
        self.apply_filters_button = QPushButton("Установить фильтры", self)
        # self.apply_filters_button.clicked.connect(self.apply_filters)

        self.clear_filters_button = QPushButton("Очистить фильтры", self)
        # self.clear_filters_button.clicked.connect(self.clear_filters)

        # Поле предпросмотра
        self.preview_area = QTextEdit(self)
        self.preview_area.setReadOnly(True)
        self.preview_area.setPlainText("Здесь будет предварительный просмотр отчета.")

        # Основной макет
        main_layout = QVBoxLayout()

        # Макет для выбора имени файла и кнопки выбора пути
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Имя файла:"))
        file_layout.addWidget(self.file_name_line_edit)
        file_layout.addWidget(self.browse_button)

        # Лейбл и комбобоксы для фильтров
        filter_box = QVBoxLayout()
        filter_box.addWidget(QLabel("Фильтры"))
        filter_box.addWidget(self.filter_combobox_1)
        filter_box.addWidget(self.filter_combobox_2)
        filter_box.addWidget(self.filter_combobox_3)
        filter_box.addWidget(self.filter_combobox_4)
        filter_box.addWidget(self.filter_combobox_5)

        # Отступ между фильтрами и кнопками
        filter_box.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        # Макет для кнопок установки и очистки фильтров
        filter_buttons_layout = QHBoxLayout()
        filter_buttons_layout.addWidget(self.apply_filters_button)
        filter_buttons_layout.addWidget(self.clear_filters_button)

        # Добавление кнопок в макет с фильтрами
        filter_box.addLayout(filter_buttons_layout)
        filter_box.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        # Макет для фильтров и предпросмотра рядом друг с другом
        preview_layout = QHBoxLayout()
        preview_layout.addLayout(filter_box)  # Добавляем фильтры слева
        preview_layout.addWidget(self.preview_area)  # Предпросмотр справа

        # Установка политики размера для предпросмотра
        self.preview_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # Макет для кнопок сохранения и отмены
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )
        button_layout.addWidget(self.ui.pushButton_save)
        button_layout.addWidget(self.ui.pushButton_cancel)

        # Добавление всех макетов в основной
        main_layout.addLayout(file_layout)
        main_layout.addLayout(preview_layout)
        main_layout.addLayout(button_layout)

        # Применяем основной макет
        self.setLayout(main_layout)

        # Подключение кнопок к функциям
        self.ui.pushButton_save.clicked.connect(self.create_report)
        self.ui.pushButton_cancel.clicked.connect(self.confirm_close)

    def browse_file(self):
        default_file_name = self.file_name_line_edit.text()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            default_file_name,
            "Документы Word (*.docx);;Все файлы (*)",
        )
        if file_name:
            # Полный путь сохраняем в атрибут
            self.file_path = file_name
            name_only = file_name.split("/")[-1]
            self.file_name_line_edit.setText(name_only)

    def update_preview(self):
        selected_filter = (
            self.filter_combobox_1.currentText()
            and self.filter_combobox_2.currentText()
            and self.filter_combobox_3.currentText()
            and self.filter_combobox_4.currentText()
            and self.filter_combobox_5.currentText()
        )
        self.preview_area.setPlainText(f"Предпросмотр для: {selected_filter}")

    def confirm_close(self):
        if (
            self.filter_combobox_1.currentIndex() != 0
            or self.filter_combobox_2.currentIndex() != 0
            or self.filter_combobox_3.currentIndex() != 0
            or self.filter_combobox_4.currentIndex() != 0
            or self.filter_combobox_5.currentIndex() != 0
        ):
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Подтверждение")
            msg_box.setText(
                "Вы действительно хотите закрыть окно? Все изменения будут потеряны."
            )
            yes_button = msg_box.addButton("Да", QMessageBox.ButtonRole.YesRole)
            msg_box.addButton("Нет", QMessageBox.ButtonRole.NoRole)
            msg_box.exec()
            if msg_box.clickedButton() == yes_button:
                self.close()
        else:
            self.close()

    def create_report(self):
        file_path = getattr(self, "file_path", "").strip()
        if not file_path:
            self.show_notification("Пожалуйста, выберите файл и путь для сохранения.")
            return
        try:
            # Проверка доступности файла
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r+"):
                        pass
                except IOError:
                    self.show_notification(
                        "Файл уже используется. Закройте его перед записью."
                    )
                    return

            if not file_path.endswith(".docx"):
                file_path += ".docx"
            print(f"Сохраняем отчёт в: {file_path}")
            make_report(file_path)
            self.show_notification("Отчёт успешно сохранён!")
        except Exception as e:
            self.show_notification(f"Ошибка при сохранении отчета: {e}")

    def show_notification(self, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Уведомление")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setFixedHeight(500)
        msg_box.exec()


def make_report(file_path):
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

        doc.save(file_path)

    print("Отчет успешно создан и сохранен.")


def set_table_width(table):
    for row in table.rows:
        for cell in row.cells:
            # Устанавливаем ширину ячейки равной её контенту
            cell.width = Pt(0)  # Автоматически подстраивает по контенту
            # Убираем обтекание текста
            cell.paragraphs[0].paragraph_format.space_after = 0
