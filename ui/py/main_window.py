# Form implementation generated from reading ui file 'ui\qt\mainWindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1282, 862)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setAutoFillBackground(True)
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.tab_1)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setKerning(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(parent=self.tab_1)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_3.addWidget(self.lineEdit_3, 1, 0, 1, 1)
        self.tableView_2 = QtWidgets.QTableView(parent=self.tab_2)
        self.tableView_2.setObjectName("tableView_2")
        self.gridLayout_3.addWidget(self.tableView_2, 2, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_4.addWidget(self.lineEdit_4, 1, 0, 1, 1)
        self.tableView_3 = QtWidgets.QTableView(parent=self.tab_3)
        self.tableView_3.setObjectName("tableView_3")
        self.gridLayout_4.addWidget(self.tableView_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.tab_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(parent=self.tab_4)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.tableView_4 = QtWidgets.QTableView(parent=self.tab_4)
        self.tableView_4.setObjectName("tableView_4")
        self.gridLayout_5.addWidget(self.tableView_4, 3, 0, 1, 2)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.tab_4)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_5.addWidget(self.lineEdit, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1282, 22))
        self.menubar.setDefaultUp(True)
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")
        self.main_data = QtWidgets.QMenu(parent=self.menubar)
        self.main_data.setObjectName("main_data")
        self.analytics = QtWidgets.QMenu(parent=self.menubar)
        self.analytics.setObjectName("analytics")
        self.export_2 = QtWidgets.QMenu(parent=self.menubar)
        self.export_2.setObjectName("export_2")
        self.about = QtWidgets.QMenu(parent=self.menubar)
        self.about.setObjectName("about")
        MainWindow.setMenuBar(self.menubar)
        self.menubar.addAction(self.main_data.menuAction())
        self.menubar.addAction(self.analytics.menuAction())
        self.menubar.addAction(self.export_2.menuAction())
        self.menubar.addAction(self.about.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Введите текст"))
        self.label_2.setText(_translate("MainWindow", "Поиск"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Таблица1")
        )
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Введите текст"))
        self.label_3.setText(_translate("MainWindow", "Поиск"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Таблица 2")
        )
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "Введите текст"))
        self.label_4.setText(_translate("MainWindow", "Поиск"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Таблица 3")
        )
        self.label.setText(_translate("MainWindow", "Поиск "))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Введите текст"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Таблица 4")
        )
        self.main_data.setTitle(_translate("MainWindow", "Данные"))
        self.analytics.setTitle(_translate("MainWindow", "Анализ"))
        self.export_2.setTitle(_translate("MainWindow", "Отчёты"))
        self.about.setTitle(_translate("MainWindow", "О программе"))