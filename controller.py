from PyQt6.QtWidgets import QMainWindow
from nursezim.pyqt.voting import Ui_MainWindow
from nursezim.pyqt.login import Ui_LoginWindow
from nursezim.pyqt.vote import Ui_VoteWindow
from dao.user_dao import UserDAO
from dao.election_dao import ElectionDAO
from dao.candidate_dao import CandidateDAO
from dao.votes_dao import VotesDAO
from classes.election import Election
from classes.candidate import Candidate
from model import Model
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtGui import QBrush
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox





class Controller(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main_window = None
        self.login_window = None
        self.vote_window = None
        self.ui_main = Ui_MainWindow()
        self.ui_login = Ui_LoginWindow()
        self.ui_vote = Ui_VoteWindow()
        self.model = Model()
        self.dao = UserDAO("/Users/argenkulzhanov/Desktop/Designer/nursezim/vote.sqlite")
        self.election = ElectionDAO("/Users/argenkulzhanov/Desktop/Designer/nursezim/vote.sqlite")
        self.candidate = CandidateDAO("/Users/argenkulzhanov/Desktop/Designer/nursezim/vote.sqlite")
        self.vote = VotesDAO("/Users/argenkulzhanov/Desktop/Designer/nursezim/vote.sqlite")
        self.email = None
        self.reset_code = None
        self.election_name = None
        self.current_account = None
        self.candidate_list = []


    def show_main_window(self):
        self.main_window = QMainWindow()
        self.ui_main.setupUi(self.main_window)
        self.init_main_window_buttons()
        self.main_window.show()
        self.ui_main.tabWidget.setCurrentIndex(0)

    def show_vote_window(self):
        self.vote_window = QMainWindow()
        self.ui_vote.setupUi(self.vote_window)
        self.vote_window.show()
        self.ui_vote.pushButton.clicked.connect(self.cast_vote)


    def init_main_window_buttons(self):
        self.ui_main.pushButton_4.clicked.connect(self.set_home)
        self.ui_main.pushButton_5.clicked.connect(self.create_election)
        self.ui_main.pushButton_2.clicked.connect(self.show_login_window)
        self.ui_main.pushButton_6.clicked.connect(self.message)
        self.ui_main.pushButton_3.clicked.connect(self.task)
        self.ui_main.pushButton_7.clicked.connect(self.go_show_vote_window)
        self.ui_main.pushButton_8.clicked.connect(self.add_candidates)
        self.ui_main.pushButton_9.clicked.connect(self.check_at_least_two_candidates)
        self.ui_main.tabWidget.tabBar().hide()

    def cast_vote(self):
        candidate_id_text = self.ui_vote.lineEdit.text()

        if not candidate_id_text:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Candidate ID is empty")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        try:
            candidate_id = int(candidate_id_text)
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Invalid Candidate ID")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        if not self.current_account:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("You need to log in")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        else:
            candidate = self.candidate.get_candidate_id(int(candidate_id_text))
            if not candidate:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("Candidate with this ID does not exist")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()

            else:

                election_name1 = self.ui_main.lineEdit_14.text()
                if self.vote.has_already_voted(self.current_account, election_name1):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setText("You have already voted")
                    msg.setWindowTitle("Error")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()

                else:
                    self.vote.save_vote(self.current_account, election_name1, int(candidate_id_text))
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setText("Vote saved successfully")
                    msg.setWindowTitle("Information")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()

    def go_show_vote_window(self):
        name = self.ui_main.lineEdit_14.text()
        if name != "":
            name_of_election = self.election.find_by_name(name)
            if name_of_election:
                self.show_vote_window()

                self.display_candidates_by_election(name)


            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setText("Election name  not found")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.exec()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Name of election is empty")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

    def display_candidates_by_election(self, election_name: str):
        candidates = self.candidate.get_candidates_by_election(election_name)

        self.ui_vote.tableWidget.setRowCount(len(candidates))
        self.ui_vote.tableWidget.setColumnCount(5)
        self.ui_vote.tableWidget.setHorizontalHeaderLabels(["Candidate ID","Election Name", "Name", "Party", "Profile"])

        header_font = self.ui_vote.tableWidget.horizontalHeader().font()
        header_font.setBold(True)
        self.ui_vote.tableWidget.horizontalHeader().setFont(header_font)
        self.ui_vote.tableWidget.setStyleSheet("QHeaderView::section { color: black; }")

        for row_index, candidate in enumerate(candidates):
            item_id = QTableWidgetItem(str(candidate.get_id()))
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui_vote.tableWidget.setItem(row_index, 0, item_id)

            item_election_name = QTableWidgetItem(candidate.get_election_name())
            item_election_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui_vote.tableWidget.setItem(row_index, 1, item_election_name)

            item_name = QTableWidgetItem(candidate.get_name())
            item_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui_vote.tableWidget.setItem(row_index, 2, item_name)

            item_party = QTableWidgetItem(candidate.get_party())
            item_party.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui_vote.tableWidget.setItem(row_index, 3, item_party)

            item_profile = QTableWidgetItem(candidate.get_profile())
            item_profile.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui_vote.tableWidget.setItem(row_index, 4, item_profile)

            for col_index in range(5):
                item = self.ui_vote.tableWidget.item(row_index, col_index)
                if item:
                    item.setForeground(QBrush(Qt.GlobalColor.black))

        self.ui_vote.tableWidget.resizeColumnsToContents()
        self.ui_vote.tableWidget.resizeRowsToContents()

        self.ui_vote.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui_vote.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def task(self):
        self.ui_main.tabWidget.setCurrentIndex(2)
        self.display_elections()


    def message(self):
        self.candidate_list = []
        self.election_name = self.ui_main.lineEdit_11.text()
        start_date = self.ui_main.lineEdit_12.text()
        end_date = self.ui_main.lineEdit_13.text()
        c = 0

        if not self.election_name:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Name of election is empty")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            c+=1



        if not self.model.validate_date_format(start_date):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Start date format is invalid. Use yyyy-MM-dd, HH:mm:ss")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            c+=1

        if not self.model.validate_date_format(end_date):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("End date format is invalid. Use yyyy-MM-dd, HH:mm:ss")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            c+=1


        if c == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Election added")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            election = Election(self.election_name, start_date, end_date)
            self.election.insert(election)
            self.ui_main.lineEdit_11.clear()
            self.ui_main.lineEdit_12.clear()
            self.ui_main.lineEdit_13.clear()

        self.ui_main.tabWidget.setCurrentIndex(3)

    def add_candidates(self):
        name_of_election = self.election_name
        name_of_candidate = self.ui_main.lineEdit_15.text()
        party = self.ui_main.lineEdit_16.text()
        profile = self.ui_main.lineEdit_18.text()

        if not name_of_candidate or not name_of_election or not party or not profile:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Input something")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("Candidate added")
            msg.setWindowTitle("Information")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
            candidate = Candidate(name_of_election, name_of_candidate, party, profile)
            self.candidate.insert(candidate)
            self.candidate_list.append(candidate)

    def check_at_least_two_candidates(self):
        if len(self.candidate_list) < 2:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("You need to add at least 2 candidates")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            self.ui_main.tabWidget.setCurrentIndex(0)
            self.ui_main.lineEdit_15.clear()
            self.ui_main.lineEdit_16.clear()
            self.ui_main.lineEdit_18.clear()

    def display_elections(self):
        elections = self.election.get_all_elections()

        if elections is None or len(elections) == 0:
            print("No elections found")
            return

        self.ui_main.tableWidget.setRowCount(len(elections))
        self.ui_main.tableWidget.setColumnCount(3)
        self.ui_main.tableWidget.setHorizontalHeaderLabels(["Name of Election", "Start Date", "End Date"])

        header_font = self.ui_main.tableWidget.horizontalHeader().font()
        header_font.setBold(True)
        self.ui_main.tableWidget.horizontalHeader().setFont(header_font)
        self.ui_main.tableWidget.setStyleSheet("QHeaderView::section { color: black; }")

        for row_index, election in enumerate(elections):
            if len(election) < 3:
                print(f"Skipping incomplete election data at row {row_index}")
                continue

            for col_index, value in enumerate(election[1:]):
                if row_index < len(elections) and col_index < 3:
                    item = QTableWidgetItem(str(value))
                    item.setForeground(QBrush(Qt.GlobalColor.black))

                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.ui_main.tableWidget.setItem(row_index, col_index, item)

        self.ui_main.tableWidget.setStyleSheet("""
            QTableWidget {
                border: 2px solid black;  /* Граница для каждой ячейки */
                padding: 5px;  /* Отступы внутри ячеек */
            }
            QTableWidget::item {
                border: 1px solid black;  /* Граница для каждой ячейки */
                padding: 5px;  /* Отступы внутри ячеек */
            }
        """)
        self.ui_main.tableWidget.resizeColumnsToContents()
        self.ui_main.tableWidget.resizeRowsToContents()

        self.ui_main.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui_main.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def set_home(self):
        self.ui_main.tabWidget.setCurrentIndex(0)

    def create_election(self):
        self.ui_main.tabWidget.setCurrentIndex(1)

    def show_login_window(self):
        self.login_window = QMainWindow()
        self.ui_login.setupUi(self.login_window)
        self.init_login_window_buttons()
        self.login_window.show()

    def init_login_window_buttons(self):
        self.ui_login.pushButton_3.clicked.connect(self.switch_to_tab_login)
        self.ui_login.pushButton_4.clicked.connect(self.switch_to_tab_create_account)
        self.ui_login.pushButton_6.clicked.connect(self.create_account)
        self.ui_login.pushButton_8.clicked.connect(self.on_cancel_create_account_clicked)
        self.ui_login.pushButton_9.clicked.connect(self.on_cancel_create_account_clicked)
        self.ui_login.pushButton_10.clicked.connect(self.login_account)
        self.ui_login.pushButton_11.clicked.connect(self.on_forgot_password_clicked)
        self.ui_login.pushButton_12.clicked.connect(self.on_cancel_clicked)
        self.ui_login.pushButton_17.clicked.connect(self.on_send_code_clicked)
        self.ui_login.pushButton_18.clicked.connect(self.on_cancel_create_account_clicked)
        self.ui_login.pushButton_31.clicked.connect(self.change_password)
        self.ui_login.pushButton_32.clicked.connect(self.on_check_code_clicked)
        self.set_visible()
        self.ui_login.tabWidget.tabBar().hide()
        self.ui_login.tabWidget.setCurrentIndex(0)

    def set_visible(self):
        self.ui_login.label_10.setVisible(False)
        self.ui_login.label_13.setVisible(False)
        self.ui_login.label_14.setVisible(False)
        self.ui_login.label_15.setVisible(False)
        self.ui_login.label_12.setVisible(False)
        self.ui_login.label_11.setVisible(False)
        self.ui_login.label_19.setVisible(False)
        self.ui_login.label_20.setVisible(False)
        self.ui_login.label_21.setVisible(False)

    def switch_to_tab_login(self):
        self.ui_login.tabWidget.setCurrentIndex(1)

    def switch_to_tab_create_account(self):
        self.ui_login.tabWidget.setCurrentIndex(2)

    def on_cancel_create_account_clicked(self):
        self.ui_login.tabWidget.setCurrentIndex(0)
        self.set_visible()

    def login_account(self):
        username = self.ui_login.lineEdit_15.text()
        password = self.ui_login.lineEdit_16.text()
        self.set_visible()
        self.current_account = username

        if self.dao.find_by_username(username) == None:
            self.ui_login.label_10.setText("Wrong username")
            self.ui_login.label_10.setVisible(True)

        else:
            my_password = self.dao.find_by_username(username).get_password()
            if password != my_password:
                self.ui_login.label_10.setText("Wrong password")
                self.ui_login.label_10.setVisible(True)

            else:
                self.ui_login.label_10.setVisible(False)
                self.ui_login.label_11.setText("Successfully login")
                self.ui_login.label_11.setVisible(True)
                QTimer.singleShot(2000, self.login_window.close)
                username = self.model.len_of_username(username)
                self.ui_main.pushButton_2.setText(username)

    def on_forgot_password_clicked(self):
        self.ui_login.tabWidget.setCurrentIndex(3)

    def on_cancel_clicked(self):
        self.login_window.close()

    def create_account(self):
        self.set_visible()
        username = self.ui_login.lineEdit_13.text()
        email = self.ui_login.lineEdit_14.text()
        password = self.ui_login.lineEdit_9.text()
        phone_number = self.ui_login.lineEdit_10.text()

        result = self.model.create_account( username, email,  password, phone_number)

        if result["success"]:
            self.dao.insert(self.model.users[username])
            self.ui_login.tabWidget.setCurrentIndex(1)

        else:
            for error_message, label_name in result["errors"]:
                label = getattr(self.ui_login, label_name)
                label.setText(error_message)
                label.setVisible(True)

    def on_send_code_clicked(self):
        self.set_visible()
        self.email = self.ui_login.lineEdit_17.text()
        if self.email != "":
            result = self.dao.find_by_email(self.email)
            if result is not None:
                self.reset_code = self.model.send_reset_password(self.email)
                self.ui_login.lineEdit_17.setEnabled(False)
                self.ui_login.label_19.setText("Code is sent to your email")
                self.ui_login.label_19.setVisible(True)
                self.ui_login.lineEdit_18.setVisible(True)


            else:
                self.ui_login.label_20.setText("Email not found")
                self.ui_login.label_20.setVisible(True)
        else:
            self.ui_login.label_20.setText("Input something")
            self.ui_login.label_20.setVisible(True)

    def on_check_code_clicked(self):
        if int(self.ui_login.lineEdit_18.text()) == self.reset_code:
            self.ui_login.tabWidget.setCurrentIndex(4)
            self.ui_login.lineEdit_17.setEnabled(True)

    def change_password(self):
        self.set_visible()
        password = self.ui_login.lineEdit_30.text()
        confirm_password = self.ui_login.lineEdit_29.text()
        if password == confirm_password:
            if self.model.is_strong_password(password):
                self.dao.update_password(self.email, password)
                self.switch_to_tab_login()
            else:
                self.ui_login.label_21.setText("Passwords is weak")
                self.ui_login.label_21.setVisible(True)
        else:
            self.ui_login.label_21.setText("Passwords do not match")
            self.ui_login.label_21.setVisible(True)