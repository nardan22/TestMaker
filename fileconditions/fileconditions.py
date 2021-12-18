from fileconditions.fileconditions_ui import *


class FileConditions(QtWidgets.QWidget):
    # Начальная инициализация
    def __init__(self, parent = None):
        super(FileConditions, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show_window()

        self.ui.closeBtn.clicked.connect(self.close_file_conditions_page)

    # Закрытие окна
    def close_file_conditions_page(self):
        self.close()

    def show_window(self):
        self.show()