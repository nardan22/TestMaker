from testpage.my_qlabel import MyQLabel
from testpage.question import Question
from testpage.testpage_ui import *
import os
import xml.etree.cElementTree as xml


class TestWindow(QtWidgets.QMainWindow):

    # Начальная инициализация
    def __init__(self, parent=None):
        # Настройка UI
        super(TestWindow, self).__init__(parent)
        self.ui = Ui_TestWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_choose_test)
        self.ui.next_question_btn.setEnabled(False)

        # Дополнительные переменные
        self.PATH_TO_TESTS = "All tests"
        self.STATISTIC_FOLDER_PATH = "Statistica"
        self.STATISTICA_SUFFIX = "_stat"
        self.PROGRAM_DATA_PATH = os.path.join(os.getenv('APPDATA'), 'Test Generator')
        self.XML_EXTENSION = '.xml'
        self.testname_path_dict = None
        self.questions = list()
        self.current_question_index = 0
        self.question_number = 0
        self.rb_group = QtWidgets.QButtonGroup()
        self.label_group = list()
        self.test_result = list()
        self.priority_indexes = list()
        self.test_progress_text = "Вопрос {question_position} / {questions_count}"

        # Методы которых надо выполнить при инициализации
        self.get_all_tests_titles_list()

        # Соединение методов событий клика элементов
        self.ui.nav_to_page_user_btn.clicked.connect(self.switch_to_user_data_page)
        self.ui.nav_to_page_choose_test.clicked.connect(self.switch_to_test_choosing_page)
        self.ui.nav_to_page_questions.clicked.connect(self.switch_to_test_question_page)
        self.ui.spisok_testov.currentTextChanged.connect(self.selected_item_of_spisok_testov_changed)
        self.ui.next_question_btn.clicked.connect(self.next_question_button_clicked)
        self.ui.answer_btn.clicked.connect(self.answer_button_clicked)
        self.ui.test_window_close_btn.clicked.connect(self.close_test_window)

    # Переход на страницу ввода имени Пользователя
    def switch_to_user_data_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_user)

    # Переход на страницу выбора Теста
    def switch_to_test_choosing_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_choose_test)

    # Переход на страницу с вопросами выбранного Теста
    def switch_to_test_question_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_questions)

        self.get_questions_from_file()
        self.get_priority_from_statistic_file()

        if len(self.priority_indexes) == 0:
            self.next_question(self.current_question_index)
        else:
            self.current_question_index = self.priority_indexes[self.question_number]
            self.next_question(self.current_question_index)

    # Переход на страницу результата тестирования
    def switch_to_result_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_result)

        self.fill_test_result()
        self.update_statistic_file()

    # При изменении выбранного Теста, обновляется список Разделов
    def selected_item_of_spisok_testov_changed(self):
        self.update_spisok_razdelov()

    # Нажатие кнопки Следующий
    def next_question_button_clicked(self):
        self.ui.next_question_btn.setEnabled(False)
        self.ui.answer_btn.setEnabled(True)

        # Чистим gridlayout и группу радио кнопок
        self.update_uis_for_next_question()

        self.question_number += 1

        if len(self.priority_indexes) == 0:
            self.current_question_index = self.question_number
        else:
            if self.question_number < len(self.priority_indexes):
                self.current_question_index = self.priority_indexes[self.question_number]

        #  Показать следующий вопрос если это не последний вопрос
        if self.question_number != len(self.questions):
            self.next_question(self.current_question_index)
        else:
            # Показать страницу результата после последнего вопроса
            self.switch_to_result_page()

    # Нажатие на кнопку Ответить
    def answer_button_clicked(self):
        self.ui.next_question_btn.setEnabled(True)
        self.ui.answer_btn.setEnabled(False)

        choosed_answer_index = -1
        for i in range(0, len(self.rb_group.buttons())):
            if self.rb_group.buttons()[i].isChecked():
                choosed_answer_index = i
                break

        if choosed_answer_index != -1:
            # Если выбранный вариант ответа не совпадается с правильным ответом, меняем цвет выбранного варианта
            if choosed_answer_index != self.questions[self.current_question_index].right_answer_index:
                self.label_group[choosed_answer_index].setStyleSheet('color: #FF1300')
            else:
                # Если выбранный ответ правильный
                self.test_result[self.current_question_index] = 1 # За правильный ответ 0 меняем на 1

        # Красим правильный вариант в зеленый цвет
        self.label_group[self.questions[self.current_question_index].right_answer_index].setStyleSheet('color: #00BD39')

    # При нажатии на вариант ответа, то Пометка радио кнопки переходит на эту строку
    def answer_text_label_clicked(self):
        label = self.sender()

        for i in range(len(self.label_group)):
            if label == self.label_group[i]:
                self.rb_group.buttons()[i].setChecked(True)
                break

    # Вспомогательные методы -----------------------------------------------------------------------------------------
    # Получает из файлов xml все заголовки тестов
    def get_all_tests_titles_list(self):
        # create new or clear existing
        if self.testname_path_dict is None:
            self.testname_path_dict = dict()
        else:
            self.testname_path_dict.clear()

        # Если папки Test Generator и Test Generator/All tests не найдены, то создаем
        os.makedirs(self.PROGRAM_DATA_PATH, exist_ok=True)
        os.makedirs(os.path.join(self.PROGRAM_DATA_PATH, self.PATH_TO_TESTS), exist_ok=True)

        my_xml_test_files_path = os.path.join(self.PROGRAM_DATA_PATH, self.PATH_TO_TESTS)

        for file_name in os.listdir(my_xml_test_files_path):
            if not file_name.endswith('.xml'): continue
            full_name = os.path.join(my_xml_test_files_path, file_name)
            tree = xml.parse(full_name)
            root = tree.getroot()
            self.testname_path_dict[root.text] = full_name

        self.update_test_list()
        self.update_spisok_razdelov()

    # Обновляет список тестов
    def update_test_list(self):
        # Clear if list is not empty
        if self.ui.spisok_testov.count() > 0:
            self.ui.spisok_testov.clear()

        # add test list
        self.ui.spisok_testov.addItems(self.testname_path_dict.keys())

    # Обновляет список разделов
    def update_spisok_razdelov(self):
        root = self.get_root_from_xml_file()
        razdely = root.findall('razdel')

        if self.ui.spisok_razdelov.count() > 0:
            self.ui.spisok_razdelov.clear()

        for razdel in razdely:
            self.ui.spisok_razdelov.addItem(razdel.text)

    # Получает из файла xml все вопросы по выбранному Тесту и Разделу
    def get_questions_from_file(self):
        if len(self.questions) > 0:
            self.questions.clear()

        root = self.get_root_from_xml_file()
        razdely = root.findall('razdel')

        for razdel in razdely:
            if razdel.text == self.ui.spisok_razdelov.currentText():
                self.ui.label_razdel.setText(razdel.text)

                for question in razdel.findall('vopros'):
                    cur_question = Question()
                    cur_question.question = question.text

                    index = 0
                    otvet_list = list()

                    for otvet in question.findall('otvet'):
                        otvet_list.append(otvet.text)
                        if 'status' in otvet.attrib:
                            cur_question.right_answer_index = index
                        index += 1

                    cur_question.answers = otvet_list
                    self.questions.append(cur_question)

                self.test_result = [0] * len(self.questions)
                break

    # Получает Корневой элемент из XML файла
    def get_root_from_xml_file(self):
        tree = xml.parse(self.testname_path_dict[self.ui.spisok_testov.currentText()])
        return tree.getroot()

    # Следующий вопрос
    def next_question(self, question_index):
        self.ui.progress_label.setText(self.test_progress_text.format(question_position = str(self.question_number + 1),
                                                                      questions_count = str(len(self.questions))))
        self.ui.label_question.setText(str(self.question_number + 1) + '. ' + self.questions[question_index].question)

        answers = self.questions[question_index].answers

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        i = 0
        for i in range(0, len(answers)):
            answer_text_radio_button = QtWidgets.QRadioButton()
            answer_text_label = MyQLabel(str(i + 1) + '. ' + answers[i])
            answer_text_label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                                                  QtWidgets.QSizePolicy.Preferred))
            answer_text_label.setWordWrap(True)
            answer_text_label.setFont(font)
            answer_text_label.setMargin(0)
            self.rb_group.addButton(answer_text_radio_button)
            self.ui.gridLayout.addWidget(answer_text_radio_button, i, 0, 1, 1)
            self.ui.gridLayout.addWidget(answer_text_label, i, 1, 1, 25)

            answer_text_label.clicked.connect(self.answer_text_label_clicked)
            self.label_group.append(answer_text_label)

    # Чистка от Виджетов перед формированием следующего вопроса
    def update_uis_for_next_question(self):
        if len(self.label_group) > 0:
            self.label_group.clear()

        if len(self.rb_group.buttons()) > 0:
            for i in reversed(range(len(self.rb_group.buttons()))):
                self.rb_group.removeButton(self.rb_group.buttons()[i])

        for i in reversed(range(self.ui.gridLayout.count())):
            self.ui.gridLayout.itemAt(i).widget().setParent(None)

    # Заполнить результат теста
    def fill_test_result(self):
        self.ui.res_test_name_value.setText(self.ui.spisok_testov.currentText())
        self.ui.res_razdel_value.setText(self.ui.spisok_razdelov.currentText())
        self.ui.res_test_count_value.setText(str(len(self.questions)))
        self.ui.res_correct_answers_count_value.setText(str(sum(self.test_result)))
        self.\
            ui.\
            res_percentage_of_correct_answers_value.\
            setText(str(round(sum(self.test_result) * 100.00 / len(self.questions))))

    # Обновить статистику
    def update_statistic_file(self):

        # Если папка AppData/Roaming/Test Generator не найдена, то создаем папку
        if not os.path.exists(self.PROGRAM_DATA_PATH):
            os.mkdir(self.PROGRAM_DATA_PATH)

        # Если папка AppData/Roaming/Test Generator/Statistica не найдена, то создаем папку
        if not os.path.exists(os.path.join(self.PROGRAM_DATA_PATH, self.STATISTIC_FOLDER_PATH)):
            os.mkdir(os.path.join(self.PROGRAM_DATA_PATH, self.STATISTIC_FOLDER_PATH))

        # Путь к файлу статистики текущего теста
        stat_file_path = os.path.join(os.path.join(self.PROGRAM_DATA_PATH, self.STATISTIC_FOLDER_PATH),
                                      self.ui.spisok_testov.currentText() + self.STATISTICA_SUFFIX + self.XML_EXTENSION)

        # Если файл статистики пройденного теста не найдена, то создаем новый файл
        if not os.path.exists(stat_file_path):
            self.create_xml_file(stat_file_path)
        else:
            tree = xml.parse(stat_file_path)
            root = tree.getroot()
            cur_razdel = None

            for razdel in root.findall('razdel'):
                if razdel.text == self.ui.spisok_razdelov.currentText():
                    voprosy = razdel.findall('vopros')
                    cur_razdel = razdel
                    for i in range(len(voprosy)):
                        if voprosy[i].text == self.questions[i].question:
                            priority = voprosy[i].find("priority")
                            if self.test_result[i] == 1:
                                priority.text = str(int(priority.text) + 1)
                            else:
                                if int(priority.text) > 0:
                                    priority.text = str(int(priority.text) - 1)
                    break

            if cur_razdel is None:
                cur_razdel = xml.SubElement(root, 'razdel')
                cur_razdel.text = self.ui.spisok_razdelov.currentText()
                for i in range(len(self.questions)):
                    vopros = xml.SubElement(cur_razdel, 'vopros')
                    vopros.text = self.questions[i].question
                    priority = xml.SubElement(vopros, 'priority')
                    priority.text = str(self.test_result[i])

            tree.write(stat_file_path)

    # Создаем XML файл, и записываем данные статистики
    def create_xml_file(self, stat_file_path):
        root = xml.Element("naimenovanie_testa", name = self.ui.spisok_testov.currentText())
        razdel = xml.SubElement(root, "razdel")
        razdel.text = self.ui.spisok_razdelov.currentText()

        for i in range(len(self.questions)):
            otvet = xml.SubElement(razdel, "vopros")
            otvet.text = self.questions[i].question

            priority = xml.SubElement(otvet, "priority")
            priority.text = str(self.test_result[i])

        tree = xml.ElementTree(root)

        with open(stat_file_path, 'wb') as file:
            tree.write(file)

    # Получить лист приоритета показа вопросов из файла статистики
    def get_priority_from_statistic_file(self):
        stat_file_path = os.path.join(os.path.join(self.PROGRAM_DATA_PATH, self.STATISTIC_FOLDER_PATH),
                                      self.ui.spisok_testov.currentText() + self.STATISTICA_SUFFIX + self.XML_EXTENSION)

        if os.path.exists(stat_file_path):

            priority_values = list()

            tree = xml.parse(stat_file_path)
            root = tree.getroot()

            for razdel in root.findall('razdel'):
                if razdel.text == self.ui.spisok_razdelov.currentText():
                    for vopros in razdel.findall('vopros'):
                        priority_values.append(int(vopros.find('priority').text))
                    break

            if len(priority_values) == 0:
                return

            max_priority = max(priority_values)
            min_priority = min(priority_values)

            for i in range(min_priority, max_priority + 1):
                for j in range(len(priority_values)):
                    if priority_values[j] == i:
                        self.priority_indexes.append(j)

    # Закрыть окно тестирования
    def close_test_window(self):
        self.close()
