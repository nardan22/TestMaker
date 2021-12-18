import ctypes
from fnmatch import fnmatch
import os
import sys

from PyQt5.QtWidgets import QMessageBox

from fileconditions.fileconditions import FileConditions
from loadfile.loadfiledialog import LoadFileDialog
from testpage.testwindow import TestWindow
from startpage_ui import *


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.load_file_page = None
        self.test_window = None
        self.load_file_conditions_page = None
        self.ALL_TESTS_DIRECTORY = 'All tests'
        self.PROGRAM_DATA_PATH = os.path.join(os.getenv('APPDATA'), 'Test Generator')
        self.SAVED_TEST_FILES_EXTENSION = '*.xml'

        self.ui.closeBtn.clicked.connect(self.close_btn_clicked)
        self.ui.newTestBtn.clicked.connect(self.load_test_file)
        self.ui.existingTestsBtn.clicked.connect(self.do_test)
        self.ui.fileConditionsBtn.clicked.connect(self.file_conditions)

    def load_test_file(self):
        self.close_alive_pages()

        self.load_file_page = LoadFileDialog()
        self.load_file_page.setModal(True)
        self.load_file_page.show()

    def do_test(self):
        self.close_alive_pages()

        if not self.__is_exist_any_test(self.SAVED_TEST_FILES_EXTENSION, self.ALL_TESTS_DIRECTORY):
            self.msg_box = QMessageBox()
            self.msg_box.setText("Не найдено ни одного теста")
            self.msg_box.setWindowTitle("Warning")
            self.msg_box.setIcon(QMessageBox.Warning)
            self.msg_box.show()
        else:
            self.test_window = TestWindow()
            self.test_window.show()

    def close_btn_clicked(self):
        self.close_alive_pages()
        self.close()

    def file_conditions(self):
        if self.load_file_conditions_page is None:
            self.load_file_conditions_page = FileConditions()
        else:
            self.load_file_conditions_page.show_window()

    def __is_exist_any_test(self, pattern, dir_name):
        os.makedirs(self.PROGRAM_DATA_PATH, exist_ok=True)
        os.makedirs(os.path.join(self.PROGRAM_DATA_PATH, dir_name), exist_ok=True)
        for root, dirs, files in os.walk(os.path.join(self.PROGRAM_DATA_PATH, dir_name)):
            for name in files:
                if fnmatch(name, pattern):
                    return True
        return False

    def close_alive_pages(self):
        if self.load_file_conditions_page is not None:
            self.load_file_conditions_page.close()

        if self.test_window is not None:
            self.test_window.close()


if __name__ == '__main__':

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.testgenerator.1_0")

    if not os.path.exists(os.path.join(os.getenv('APPDATA'), 'Test Generator')):
        os.mkdir(os.path.join(os.getenv('APPDATA'), 'Test Generator'))

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('resources/app-icon.ico'))

    myWindow = MyWindow()
    myWindow.show()

    sys.exit(app.exec())
