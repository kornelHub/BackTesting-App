import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from utilities.helpers import indicator_default_options
from pages.change_indicator_form_page import Change_Indicator_Form_Page
from PySide2.QtCore import Slot


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/define_indicator_to_plot_page.ui"))


class Define_Indicator_To_Plot_Page(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.cancel_button.clicked.connect(lambda: self.close())
        # self.delete_button.clicked.connect(lambda: self.hide_last_indicator())
        self.add_button.clicked.connect(lambda: self.show_next_indicator())

        self.delete_button_1.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.delete_button_1.setIconSize(QtCore.QSize(28, 28))
        self.delete_button_1.clicked.connect(lambda: self.hide_last_indicator(1))
        self.delete_button_1.setText('')

        self.delete_button_2.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.delete_button_2.setIconSize(QtCore.QSize(28, 28))
        self.delete_button_2.clicked.connect(lambda: self.hide_last_indicator(2))
        self.delete_button_2.setText('')

        self.delete_button_3.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.delete_button_3.setIconSize(QtCore.QSize(28, 28))
        self.delete_button_3.clicked.connect(lambda: self.hide_last_indicator(3))
        self.delete_button_3.setText('')

        self.delete_button_4.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.delete_button_4.setIconSize(QtCore.QSize(28, 28))
        self.delete_button_4.clicked.connect(lambda: self.hide_last_indicator(4))
        self.delete_button_4.setText('')

        self.delete_button_5.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.delete_button_5.setIconSize(QtCore.QSize(28, 28))
        self.delete_button_5.clicked.connect(lambda: self.hide_last_indicator(5))
        self.delete_button_5.setText('')

        self.delete_button_6.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.delete_button_6.setIconSize(QtCore.QSize(28, 28))
        self.delete_button_6.clicked.connect(lambda: self.hide_last_indicator(6))
        self.delete_button_6.setText('')

        self.widget_list = [[self.indicator_widget_nested, self.firstIndicator_comboBox, self.indicatorOptions_button],
                            [self.indicator_widget_nested_2, self.firstIndicator_comboBox_2, self.indicatorOptions_button_2],
                            [self.indicator_widget_nested_3, self.firstIndicator_comboBox_3, self.indicatorOptions_button_3],
                            [self.indicator_widget_nested_4, self.firstIndicator_comboBox_4, self.indicatorOptions_button_4],
                            [self.indicator_widget_nested_5, self.firstIndicator_comboBox_5, self.indicatorOptions_button_5],
                            [self.indicator_widget_nested_6, self.firstIndicator_comboBox_6, self.indicatorOptions_button_6]]

        self.firstIndicator_comboBox.setCurrentIndex(-1)
        self.firstIndicator_comboBox_2.setCurrentIndex(-1)
        self.firstIndicator_comboBox_3.setCurrentIndex(-1)
        self.firstIndicator_comboBox_4.setCurrentIndex(-1)
        self.firstIndicator_comboBox_5.setCurrentIndex(-1)
        self.firstIndicator_comboBox_6.setCurrentIndex(-1)

        self.indicator_widget_nested_2.hide()
        self.indicator_widget_nested_3.hide()
        self.indicator_widget_nested_4.hide()
        self.indicator_widget_nested_5.hide()
        self.indicator_widget_nested_6.hide()

        self.indicatorOptions_button.clicked.connect(lambda: self.open_form_with_indicator_options(self.firstIndicator_comboBox.currentText(), self.indicatorOptions_button.text(), self.indicatorOptions_button))
        self.indicatorOptions_button_2.clicked.connect(lambda: self.open_form_with_indicator_options(self.firstIndicator_comboBox_2.currentText(), self.indicatorOptions_button_2.text(), self.indicatorOptions_button_2))
        self.indicatorOptions_button_3.clicked.connect(lambda: self.open_form_with_indicator_options(self.firstIndicator_comboBox_3.currentText(), self.indicatorOptions_button_3.text(), self.indicatorOptions_button_3))
        self.indicatorOptions_button_4.clicked.connect(lambda: self.open_form_with_indicator_options(self.firstIndicator_comboBox_4.currentText(), self.indicatorOptions_button_4.text(), self.indicatorOptions_button_4))
        self.indicatorOptions_button_5.clicked.connect(lambda: self.open_form_with_indicator_options(self.firstIndicator_comboBox_5.currentText(), self.indicatorOptions_button_5.text(), self.indicatorOptions_button_5))
        self.indicatorOptions_button_6.clicked.connect(lambda: self.open_form_with_indicator_options(self.firstIndicator_comboBox_6.currentText(), self.indicatorOptions_button_6.text(), self.indicatorOptions_button_6))


        self.firstIndicator_comboBox.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.firstIndicator_comboBox, self.indicatorOptions_button, self.indicator_options_label))
        self.firstIndicator_comboBox_2.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.firstIndicator_comboBox_2, self.indicatorOptions_button_2, self.indicator_options_label_2))
        self.firstIndicator_comboBox_3.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.firstIndicator_comboBox_3, self.indicatorOptions_button_3, self.indicator_options_label_3))
        self.firstIndicator_comboBox_4.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.firstIndicator_comboBox_4, self.indicatorOptions_button_4, self.indicator_options_label_4))
        self.firstIndicator_comboBox_5.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.firstIndicator_comboBox_5, self.indicatorOptions_button_5, self.indicator_options_label_5))
        self.firstIndicator_comboBox_6.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.firstIndicator_comboBox_6, self.indicatorOptions_button_6, self.indicator_options_label_6))


    def hide_last_indicator(self, indicator_number_to_delete):
        visible_widgets = 0
        for x in self.widget_list:
            if x[0].isVisible():
                visible_widgets += 1

        for x in range(indicator_number_to_delete-1, visible_widgets-1):
            self.widget_list[x][1].setCurrentIndex(self.widget_list[x][1].findText(self.widget_list[x+1][1].currentText(), QtCore.Qt.MatchFixedString))
            self.widget_list[x][2].setText(self.widget_list[x+1][2].text())


        self.widget_list[visible_widgets-1][1].setCurrentIndex(-1)
        self.widget_list[visible_widgets-1][2].setText('')
        self.widget_list[visible_widgets-1][0].hide()


    def show_next_indicator(self):
        for x in range(len(self.widget_list)):
            if x == 0 and not self.widget_list[0][0].isVisible():
                self.widget_list[x][0].show()
                self.widget_list[x][1].setCurrentIndex(-1)
                self.widget_list[x][2].setText('')
                break
            elif self.widget_list[x][0].isVisible() and not self.widget_list[x + 1][0].isVisible():
                self.widget_list[x+1][0].show()
                self.widget_list[x+1][1].setCurrentIndex(-1)
                self.widget_list[x+1][2].setText('')
                break



    def autofill_indicator_option(self, combo_box, linked_option_edit, linked_label):
        if combo_box.currentText() == "Value (Plain integer or double)" \
                or combo_box.currentText() == 'Open (Open price of candle)' \
                or combo_box.currentText() == 'High (High price of candle)' \
                or combo_box.currentText() == 'Low (Low price of candle)' \
                or combo_box.currentText() == 'Close (Close price of candle)'\
                or combo_box.currentText() == 'Volume (Amount traded in amount of time)':
            linked_label.setText('Value:')
            linked_option_edit.setText(indicator_default_options.get(combo_box.currentText()))
        else:
            linked_label.setText('Options:')
            linked_option_edit.setText(indicator_default_options.get(combo_box.currentText()))

        if indicator_default_options.get(combo_box.currentText()) == '(-)':
            linked_option_edit.setEnabled(False)
        else:
            linked_option_edit.setEnabled(True)


    def open_form_with_indicator_options(self, indicator, typed_options, qlineedit_field):
        recive_indicator_options_object = Recive_Indicator_Options()
        change_indicator_form_page = Change_Indicator_Form_Page()
        change_indicator_form_page.set_up_view(indicator, typed_options, qlineedit_field, recive_indicator_options_object)
        change_indicator_form_page.show()


class Recive_Indicator_Options(QtCore.QObject):
    @Slot(str)
    def recive_indicator_options(self, indicator_option, qlineedit_field):
        qlineedit_field.setText(indicator_option)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Define_Indicator_To_Plot_Page()
    w.show()
    sys.exit(app.exec_())