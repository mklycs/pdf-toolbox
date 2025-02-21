from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QLineEdit, QLabel, QPushButton, QSpacerItem
from PySide6.QtCore import Qt
from popups.popup_info import PopupInfo
from other.funcs import Funcs
import os

class ViewEnterPassword(QWidget):
    def __init__(self, switch_to_menu, filepath):
        super().__init__()

        self.switch_to_menu = switch_to_menu
        self.filepath = filepath
        
    def open_pdf(self):
        self.funcs = Funcs()
        self.pdfReader = self.funcs.check_if_protected(self.filepath)
        if not self.pdfReader:
            popupInfo = PopupInfo("Failed to open the file with the provided password.")
            return None
        else:
            return True

    def submit_password(self):
        password = self.inputfield.text()
        status = self.funcs.protect_pdf(self.pdfReader, self.filepath, password)

        popupInfo = PopupInfo(status)
        # self.submitButton.setEnabled(False)

    def add_layout(self):
        # add widgets
        gobackButton = QPushButton("  <  ")
        gobackButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        gobackButton.setObjectName("cssButton")
        gobackButton.clicked.connect(self.switch_to_menu)
            
        vSpacerAbove = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        
        label = QLabel(f"Enter password for: <br>\"{os.path.basename(self.filepath)}\"")
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
            
        self.inputfield = QLineEdit()
        self.inputfield.setEchoMode(QLineEdit.Password)

        vSpacerBelow = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        hSpacerRight = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.submitButton = QPushButton("Submit")
        self.submitButton.setObjectName("cssButton")
        self.submitButton.clicked.connect(self.submit_password)
        self.submitButton.setFixedHeight(30)
        self.submitButton.setFixedWidth(200)

        hSpacerLeft = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # add layouts
        layout = QVBoxLayout()
        submitButtonLayout = QHBoxLayout()

        # add widgets to layouts
        layout.addWidget(gobackButton)        
        layout.addItem(vSpacerAbove)
        layout.addWidget(label)
        layout.addWidget(self.inputfield)
        layout.addItem(vSpacerBelow)

        submitButtonLayout.addItem(hSpacerRight)
        submitButtonLayout.addWidget(self.submitButton)
        submitButtonLayout.addItem(hSpacerLeft)

        # add layouts to main layout
        layout.addLayout(submitButtonLayout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QPushButton#cssButton{
                background-color: #357ABD;
                color: #FFFFFF;
                border: 2px solid #2C6BC4;
                border-radius: 5px;
                padding: 3px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton#cssButton:hover{
                background-color: #2C6BC4;
            }

            QPushButton#cssButton:pressed{
                background-color: #1A4A81;
            }

            QLabel{
                color: #FFFFFF;
                font-size: 25px;
                font-family: Arial;
            }

            QLineEdit{
                border: 1px solid #3d3d3d;
                border-radius: 2px;
                font-size: 16px;
                color: #FFFFFF;
                padding-left: 2px;
                margin-right: 100px;
                margin-left: 100px;
            }
        """)