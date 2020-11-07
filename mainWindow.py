# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 600))
        MainWindow.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(1000, 600))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_top_contener = QtWidgets.QFrame(self.centralwidget)
        self.frame_top_contener.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_top_contener.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_top_contener.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_contener.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_contener.setObjectName("frame_top_contener")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_top_contener)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_toggle = QtWidgets.QFrame(self.frame_top_contener)
        self.frame_toggle.setMaximumSize(QtCore.QSize(70, 40))
        self.frame_toggle.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.frame_toggle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_toggle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_toggle.setObjectName("frame_toggle")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_toggle)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btn_toggle = QtWidgets.QPushButton(self.frame_toggle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_toggle.sizePolicy().hasHeightForWidth())
        self.btn_toggle.setSizePolicy(sizePolicy)
        self.btn_toggle.setStyleSheet("color: rgb(255, 255, 255);\n"
"border: 0px sold;")
        self.btn_toggle.setObjectName("btn_toggle")
        self.verticalLayout_2.addWidget(self.btn_toggle)
        self.horizontalLayout.addWidget(self.frame_toggle)
        self.frame_top_menu = QtWidgets.QFrame(self.frame_top_contener)
        self.frame_top_menu.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_menu.setObjectName("frame_top_menu")
        self.horizontalLayout.addWidget(self.frame_top_menu)
        self.verticalLayout.addWidget(self.frame_top_contener)
        self.frame_content = QtWidgets.QFrame(self.centralwidget)
        self.frame_content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content.setObjectName("frame_content")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_content)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_left_menu_container = QtWidgets.QFrame(self.frame_content)
        self.frame_left_menu_container.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame_left_menu_container.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.frame_left_menu_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_left_menu_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu_container.setObjectName("frame_left_menu_container")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_left_menu_container)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_left_menu = QtWidgets.QFrame(self.frame_left_menu_container)
        self.frame_left_menu.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu.setObjectName("frame_left_menu")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_4.setContentsMargins(0, 0, -1, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.btn_menu_page_1 = QtWidgets.QPushButton(self.frame_left_menu)
        self.btn_menu_page_1.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_menu_page_1.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px sold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_menu_page_1.setObjectName("btn_menu_page_1")
        self.verticalLayout_4.addWidget(self.btn_menu_page_1)
        self.btn_menu_page_2 = QtWidgets.QPushButton(self.frame_left_menu)
        self.btn_menu_page_2.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_menu_page_2.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px sold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_menu_page_2.setObjectName("btn_menu_page_2")
        self.verticalLayout_4.addWidget(self.btn_menu_page_2)
        self.btn_menu_page_3 = QtWidgets.QPushButton(self.frame_left_menu)
        self.btn_menu_page_3.setMinimumSize(QtCore.QSize(70, 40))
        self.btn_menu_page_3.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px sold;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_menu_page_3.setObjectName("btn_menu_page_3")
        self.verticalLayout_4.addWidget(self.btn_menu_page_3)
        self.verticalLayout_3.addWidget(self.frame_left_menu, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_left_menu_container)
        self.frame_pages = QtWidgets.QFrame(self.frame_content)
        self.frame_pages.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_pages.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_pages.setObjectName("frame_pages")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_pages)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.widget_pages = QtWidgets.QStackedWidget(self.frame_pages)
        self.widget_pages.setObjectName("widget_pages")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.page_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.p2_left_widget = QtWidgets.QWidget(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_left_widget.sizePolicy().hasHeightForWidth())
        self.p2_left_widget.setSizePolicy(sizePolicy)
        self.p2_left_widget.setObjectName("p2_left_widget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.p2_left_widget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.p2_leftTop_widget = QtWidgets.QWidget(self.p2_left_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_leftTop_widget.sizePolicy().hasHeightForWidth())
        self.p2_leftTop_widget.setSizePolicy(sizePolicy)
        self.p2_leftTop_widget.setObjectName("p2_leftTop_widget")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.p2_leftTop_widget)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.p2_buy_label = QtWidgets.QLabel(self.p2_leftTop_widget)
        self.p2_buy_label.setMaximumSize(QtCore.QSize(16777215, 150))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.p2_buy_label.setFont(font)
        self.p2_buy_label.setStyleSheet("QLabel {\n"
"    color: rgb(80, 220, 100);\n"
"}")
        self.p2_buy_label.setAlignment(QtCore.Qt.AlignCenter)
        self.p2_buy_label.setObjectName("p2_buy_label")
        self.verticalLayout_10.addWidget(self.p2_buy_label)
        self.p2_buyCondition_widget = QtWidgets.QWidget(self.p2_leftTop_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_buyCondition_widget.sizePolicy().hasHeightForWidth())
        self.p2_buyCondition_widget.setSizePolicy(sizePolicy)
        self.p2_buyCondition_widget.setStyleSheet("QWidget {\n"
"border: 2px solid rgb(255,255,255);\n"
"nborder-radius: 20px;\n"
"}")
        self.p2_buyCondition_widget.setObjectName("p2_buyCondition_widget")
        self.p2_buyCondition_treeWidget = QtWidgets.QTreeWidget(self.p2_buyCondition_widget)
        self.p2_buyCondition_treeWidget.setGeometry(QtCore.QRect(0, 0, 411, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_buyCondition_treeWidget.sizePolicy().hasHeightForWidth())
        self.p2_buyCondition_treeWidget.setSizePolicy(sizePolicy)
        self.p2_buyCondition_treeWidget.setStyleSheet("color: rgb(255, 255, 255);")
        self.p2_buyCondition_treeWidget.setObjectName("p2_buyCondition_treeWidget")
        self.p2_buyCondition_treeWidget.headerItem().setText(0, "1")
        self.verticalLayout_10.addWidget(self.p2_buyCondition_widget)
        self.p2_addBuyCondition_button = QtWidgets.QPushButton(self.p2_leftTop_widget)
        self.p2_addBuyCondition_button.setMinimumSize(QtCore.QSize(0, 25))
        self.p2_addBuyCondition_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 170, 255);\n"
"border: 0px sold;")
        self.p2_addBuyCondition_button.setObjectName("p2_addBuyCondition_button")
        self.verticalLayout_10.addWidget(self.p2_addBuyCondition_button)
        self.verticalLayout_8.addWidget(self.p2_leftTop_widget)
        self.p2_leftBottom_widget = QtWidgets.QWidget(self.p2_left_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_leftBottom_widget.sizePolicy().hasHeightForWidth())
        self.p2_leftBottom_widget.setSizePolicy(sizePolicy)
        self.p2_leftBottom_widget.setStyleSheet("")
        self.p2_leftBottom_widget.setObjectName("p2_leftBottom_widget")
        self.verticalLayout_8.addWidget(self.p2_leftBottom_widget)
        self.horizontalLayout_6.addWidget(self.p2_left_widget)
        self.p2_right_widget = QtWidgets.QWidget(self.page_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_right_widget.sizePolicy().hasHeightForWidth())
        self.p2_right_widget.setSizePolicy(sizePolicy)
        self.p2_right_widget.setObjectName("p2_right_widget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.p2_right_widget)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.p2_rightTop_widget = QtWidgets.QWidget(self.p2_right_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_rightTop_widget.sizePolicy().hasHeightForWidth())
        self.p2_rightTop_widget.setSizePolicy(sizePolicy)
        self.p2_rightTop_widget.setObjectName("p2_rightTop_widget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.p2_rightTop_widget)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.p2_sell_label = QtWidgets.QLabel(self.p2_rightTop_widget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.p2_sell_label.setFont(font)
        self.p2_sell_label.setStyleSheet("QLabel {\n"
"    color: rgb(185, 15, 10);\n"
"}")
        self.p2_sell_label.setAlignment(QtCore.Qt.AlignCenter)
        self.p2_sell_label.setObjectName("p2_sell_label")
        self.verticalLayout_11.addWidget(self.p2_sell_label)
        self.p2_sellCondition_widget = QtWidgets.QWidget(self.p2_rightTop_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_sellCondition_widget.sizePolicy().hasHeightForWidth())
        self.p2_sellCondition_widget.setSizePolicy(sizePolicy)
        self.p2_sellCondition_widget.setStyleSheet("QWidget {\n"
"border: 2px solid rgb(255,255,255);\n"
"nborder-radius: 20px;\n"
"}")
        self.p2_sellCondition_widget.setObjectName("p2_sellCondition_widget")
        self.p2_sellCondition_treeWidget = QtWidgets.QTreeWidget(self.p2_sellCondition_widget)
        self.p2_sellCondition_treeWidget.setGeometry(QtCore.QRect(0, 0, 401, 151))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_sellCondition_treeWidget.sizePolicy().hasHeightForWidth())
        self.p2_sellCondition_treeWidget.setSizePolicy(sizePolicy)
        self.p2_sellCondition_treeWidget.setStyleSheet("color: rgb(255, 255, 255);")
        self.p2_sellCondition_treeWidget.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.p2_sellCondition_treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.p2_sellCondition_treeWidget.setObjectName("p2_sellCondition_treeWidget")
        self.p2_sellCondition_treeWidget.headerItem().setText(0, "1")
        self.verticalLayout_11.addWidget(self.p2_sellCondition_widget)
        self.p2_addSellCondition_button = QtWidgets.QPushButton(self.p2_rightTop_widget)
        self.p2_addSellCondition_button.setMinimumSize(QtCore.QSize(0, 25))
        self.p2_addSellCondition_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 170, 255);\n"
"border: 0px sold;")
        self.p2_addSellCondition_button.setObjectName("p2_addSellCondition_button")
        self.verticalLayout_11.addWidget(self.p2_addSellCondition_button)
        self.verticalLayout_9.addWidget(self.p2_rightTop_widget)
        self.p2_rightBottom_widget = QtWidgets.QWidget(self.p2_right_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p2_rightBottom_widget.sizePolicy().hasHeightForWidth())
        self.p2_rightBottom_widget.setSizePolicy(sizePolicy)
        self.p2_rightBottom_widget.setObjectName("p2_rightBottom_widget")
        self.verticalLayout_9.addWidget(self.p2_rightBottom_widget)
        self.horizontalLayout_6.addWidget(self.p2_right_widget)
        self.widget_pages.addWidget(self.page_2)
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.p1_dataFormGrouping_widget = QtWidgets.QWidget(self.page_1)
        self.p1_dataFormGrouping_widget.setMaximumSize(QtCore.QSize(16777215, 80))
        self.p1_dataFormGrouping_widget.setObjectName("p1_dataFormGrouping_widget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.p1_dataFormGrouping_widget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.p1_dataFormTop_widget = QtWidgets.QWidget(self.p1_dataFormGrouping_widget)
        self.p1_dataFormTop_widget.setMinimumSize(QtCore.QSize(0, 40))
        self.p1_dataFormTop_widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.p1_dataFormTop_widget.setObjectName("p1_dataFormTop_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.p1_dataFormTop_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(10)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.p1_startDate_textField = QtWidgets.QLineEdit(self.p1_dataFormTop_widget)
        self.p1_startDate_textField.setStyleSheet("QLineEdit {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 20px;\n"
"    color: rgb(255, 255, 255);\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"    background-color: rgb(60, 60, 60);\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(75, 75, 75);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(85, 170, 255);\n"
"}\n"
"")
        self.p1_startDate_textField.setText("")
        self.p1_startDate_textField.setObjectName("p1_startDate_textField")
        self.horizontalLayout_4.addWidget(self.p1_startDate_textField)
        self.p1_endDate_textField = QtWidgets.QLineEdit(self.p1_dataFormTop_widget)
        self.p1_endDate_textField.setStyleSheet("QLineEdit {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 20px;\n"
"    color: rgb(255, 255, 255);\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"    background-color: rgb(60, 60, 60);\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(75, 75, 75);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(85, 170, 255);\n"
"}\n"
"")
        self.p1_endDate_textField.setText("")
        self.p1_endDate_textField.setObjectName("p1_endDate_textField")
        self.horizontalLayout_4.addWidget(self.p1_endDate_textField)
        self.verticalLayout_6.addWidget(self.p1_dataFormTop_widget)
        self.p1_dataFormBottom_widget = QtWidgets.QWidget(self.p1_dataFormGrouping_widget)
        self.p1_dataFormBottom_widget.setEnabled(True)
        self.p1_dataFormBottom_widget.setMinimumSize(QtCore.QSize(0, 40))
        self.p1_dataFormBottom_widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.p1_dataFormBottom_widget.setObjectName("p1_dataFormBottom_widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.p1_dataFormBottom_widget)
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.p1_interval_dropdown = QtWidgets.QComboBox(self.p1_dataFormBottom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p1_interval_dropdown.sizePolicy().hasHeightForWidth())
        self.p1_interval_dropdown.setSizePolicy(sizePolicy)
        self.p1_interval_dropdown.setStyleSheet("QComboBox {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 20px;\n"
"    color: rgb(255, 255, 255);\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"    background-color: rgb(60, 60, 60);\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    border: 2pxsolid rgb(45, 45, 45);\n"
"    selection-background-color:rgb(45, 45, 45);\n"
"    color: #FFF\n"
"                  }\n"
"")
        self.p1_interval_dropdown.setObjectName("p1_interval_dropdown")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.p1_interval_dropdown.addItem("")
        self.horizontalLayout_5.addWidget(self.p1_interval_dropdown)
        self.p1_cryptoSymbol_textField = QtWidgets.QLineEdit(self.p1_dataFormBottom_widget)
        self.p1_cryptoSymbol_textField.setStyleSheet("QLineEdit {\n"
"    border: 2px solid rgb(45, 45, 45);\n"
"    border-radius: 20px;\n"
"    color: rgb(255, 255, 255);\n"
"    padding-left: 20px;\n"
"    padding-right: 20px;\n"
"    background-color: rgb(60, 60, 60);\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(75, 75, 75);\n"
"}\n"
"QLineEdit:focus{\n"
"    border: 2px solid rgb(85, 170, 255);\n"
"}\n"
"")
        self.p1_cryptoSymbol_textField.setText("")
        self.p1_cryptoSymbol_textField.setObjectName("p1_cryptoSymbol_textField")
        self.horizontalLayout_5.addWidget(self.p1_cryptoSymbol_textField)
        self.p1_saveDataToFile_button = QtWidgets.QPushButton(self.p1_dataFormBottom_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.p1_saveDataToFile_button.sizePolicy().hasHeightForWidth())
        self.p1_saveDataToFile_button.setSizePolicy(sizePolicy)
        self.p1_saveDataToFile_button.setMinimumSize(QtCore.QSize(0, 0))
        self.p1_saveDataToFile_button.setMaximumSize(QtCore.QSize(16777215, 20))
        self.p1_saveDataToFile_button.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 170, 255);\n"
"border: 0px sold;")
        self.p1_saveDataToFile_button.setObjectName("p1_saveDataToFile_button")
        self.horizontalLayout_5.addWidget(self.p1_saveDataToFile_button)
        self.verticalLayout_6.addWidget(self.p1_dataFormBottom_widget)
        self.verticalLayout_5.addWidget(self.p1_dataFormGrouping_widget)
        self.p1_ohlcvPlot_widget = QtWidgets.QWidget(self.page_1)
        self.p1_ohlcvPlot_widget.setObjectName("p1_ohlcvPlot_widget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.p1_ohlcvPlot_widget)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.p1_ohlcvPlot_qWebEngineView = QtWebEngineWidgets.QWebEngineView(self.p1_ohlcvPlot_widget)
        self.p1_ohlcvPlot_qWebEngineView.setObjectName("p1_ohlcvPlot_qWebEngineView")
        self.verticalLayout_7.addWidget(self.p1_ohlcvPlot_qWebEngineView)
        self.verticalLayout_5.addWidget(self.p1_ohlcvPlot_widget)
        self.p1_ohlcvPlot_widget.raise_()
        self.p1_dataFormGrouping_widget.raise_()
        self.widget_pages.addWidget(self.page_1)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.label_3 = QtWidgets.QLabel(self.page_3)
        self.label_3.setGeometry(QtCore.QRect(270, 80, 261, 201))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.page_3)
        self.pushButton.setGeometry(QtCore.QRect(310, 260, 221, 101))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.widget_pages.addWidget(self.page_3)
        self.horizontalLayout_3.addWidget(self.widget_pages)
        self.horizontalLayout_2.addWidget(self.frame_pages)
        self.verticalLayout.addWidget(self.frame_content)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.widget_pages.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_toggle.setText(_translate("MainWindow", "TOGGLE"))
        self.btn_menu_page_1.setText(_translate("MainWindow", "Page 1"))
        self.btn_menu_page_2.setText(_translate("MainWindow", "Page 2"))
        self.btn_menu_page_3.setText(_translate("MainWindow", "Page 3"))
        self.p2_buy_label.setText(_translate("MainWindow", "Buy"))
        self.p2_addBuyCondition_button.setText(_translate("MainWindow", "+ Add "))
        self.p2_sell_label.setText(_translate("MainWindow", "Sell"))
        self.p2_addSellCondition_button.setText(_translate("MainWindow", "+ Add"))
        self.p1_startDate_textField.setPlaceholderText(_translate("MainWindow", "Start date"))
        self.p1_endDate_textField.setPlaceholderText(_translate("MainWindow", "End date"))
        self.p1_interval_dropdown.setItemText(0, _translate("MainWindow", "1m"))
        self.p1_interval_dropdown.setItemText(1, _translate("MainWindow", "3m"))
        self.p1_interval_dropdown.setItemText(2, _translate("MainWindow", "5m"))
        self.p1_interval_dropdown.setItemText(3, _translate("MainWindow", "15m"))
        self.p1_interval_dropdown.setItemText(4, _translate("MainWindow", "30m"))
        self.p1_interval_dropdown.setItemText(5, _translate("MainWindow", "1h"))
        self.p1_interval_dropdown.setItemText(6, _translate("MainWindow", "2h"))
        self.p1_interval_dropdown.setItemText(7, _translate("MainWindow", "4h"))
        self.p1_interval_dropdown.setItemText(8, _translate("MainWindow", "6h"))
        self.p1_interval_dropdown.setItemText(9, _translate("MainWindow", "8h"))
        self.p1_interval_dropdown.setItemText(10, _translate("MainWindow", "12h"))
        self.p1_interval_dropdown.setItemText(11, _translate("MainWindow", "1d"))
        self.p1_interval_dropdown.setItemText(12, _translate("MainWindow", "3d"))
        self.p1_interval_dropdown.setItemText(13, _translate("MainWindow", "1w"))
        self.p1_cryptoSymbol_textField.setPlaceholderText(_translate("MainWindow", "Cryptocurrency symbol pair", "xd1"))
        self.p1_saveDataToFile_button.setText(_translate("MainWindow", "SAVE DATA TO FILE"))
        self.label_3.setText(_translate("MainWindow", "PAGE 3"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))

from PySide2 import QtWebEngineWidgets

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

