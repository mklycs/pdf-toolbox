from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy, QFileDialog, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt
from popups.popup_info import PopupInfo
from other.funcs import Funcs
import os

class ViewMetadataInput(QWidget):
    def __init__(self, switch_to_menu, filepath):
        super().__init__()

        self.switch_to_menu = switch_to_menu
        self.filepath = filepath

        self.funcs = Funcs()

    def get_metadata(self):
        title = self.inputTitle.text()
        author = self.inputAuthor.text()
        subject = self.inputSubject.text()
        creation_date = self.inputCreationDate.text()
        mod_Date = self.inputModDate.text()
        creator = self.inputCreator.text()
        producer = self.inputProducer.text()
        
        if not (title or author or subject or creation_date or mod_Date or creator or producer):
            return {}

        creation_date = "D: " + creation_date
        mod_Date = "D: " + mod_Date
        
        metadata = {
            "/Title": title,
            "/Author": author,
            "/Subject": subject,
            "/CreationDate": creation_date,
            "/ModDate": mod_Date,
            "/Creator": creator,
            "/Producer": producer
        }

        return metadata

    def submit_data(self):
        metadata = self.get_metadata()
        outputPath, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "(*.pdf)")
        self.funcs.write_meta(self.pdfReader, self.filepath, outputPath, metadata)
        popupInfo = PopupInfo(f"Successfully changed metadata of: \"{os.path.basename(outputPath)}\".")
        self.switch_to_menu()

    def open_pdf(self):
        self.pdfReader = self.funcs.check_if_protected(self.filepath)
        if not self.pdfReader:
            popupInfo = PopupInfo("Failed to open the file with the provided password.")
            return None
        else:
            return True
    
    def add_layout(self):
        # add widgets
        gobackButton = QPushButton("  <  ")
        gobackButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        gobackButton.setObjectName("cssButton")
        gobackButton.clicked.connect(self.switch_to_menu)

        infoLabel = QLabel(f"Changing metadata of: \"{os.path.basename(self.filepath)}\"")

        self.inputTitle = QLineEdit()
        self.inputTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputTitle.setPlaceholderText("Enter new title: (Default: Unknown)")
            
        self.inputAuthor = QLineEdit()
        self.inputAuthor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputAuthor.setPlaceholderText("Enter new author: (Default: Unknown)")
            
        self.inputSubject = QLineEdit()
        self.inputSubject.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputSubject.setPlaceholderText("Enter new subject: (Default: Unknown)")
            
        self.inputCreationDate = QLineEdit()
        self.inputCreationDate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputCreationDate.setPlaceholderText("Enter new date of file creation: (proper format: YYYYMMDDHHMMSS)")
            
        self.inputModDate = QLineEdit()
        self.inputModDate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputModDate.setPlaceholderText("Enter new date of file modification: (proper format: YYYYMMDDHHMMSS)")
            
        self.inputCreator = QLineEdit()
        self.inputCreator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputCreator.setPlaceholderText("Enter new creator: (Default: Unknown)")
            
        self.inputProducer = QLineEdit()
        self.inputProducer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputProducer.setPlaceholderText("Enter new production method of file: (Default: Unknown)")

        hSpacerRight = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        submitButton = QPushButton("Overwrite")
        submitButton.setObjectName("cssButton")
        submitButton.clicked.connect(self.submit_data)
        #submitButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        submitButton.setFixedHeight(30)
        submitButton.setFixedWidth(200)

        hSpacerLeft = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        noteLabel = QLabel("Note: Overwriting the metadata of a PDF protected with a password will remove its password.")
        noteLabel.setAlignment(Qt.AlignCenter)

        # add layouts
        layout = QVBoxLayout()
        submitButtonLayout = QHBoxLayout()

        # add widgets to layouts
        layout.addWidget(gobackButton)
        layout.addWidget(infoLabel)
        layout.addWidget(self.inputTitle)
        layout.addWidget(self.inputAuthor)
        layout.addWidget(self.inputSubject)
        layout.addWidget(self.inputCreationDate)
        layout.addWidget(self.inputModDate)
        layout.addWidget(self.inputCreator)
        layout.addWidget(self.inputProducer)
        layout.addWidget(noteLabel)
        
        submitButtonLayout.addItem(hSpacerRight)
        submitButtonLayout.addWidget(submitButton)
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
                font-size: 15px;
                font-family: Arial;
                margin-top: 20px;
            }

            QLineEdit{
                color: #FFFFFF;
                border: none;
                border-bottom: 1px solid #3d3d3d;
                border-radius: 0px;
                margin-bottom: 5px;
            }
        """)