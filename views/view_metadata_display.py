from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QTextEdit, QLabel, QPushButton
from popups.popup_info import PopupInfo
from other.funcs import Funcs
import os

class ViewMetadataDisplay(QWidget):
    def __init__(self, switch_to_menu, filepath):
        super().__init__()

        self.switch_to_menu = switch_to_menu
        self.filepath = filepath
        self.funcs = Funcs()
        
    def open_pdf(self):
        pdfReader = self.funcs.check_if_protected(self.filepath)
        if not pdfReader:
            popupInfo = PopupInfo("Failed to open the file with the provided password.")
            return None
        else:
            return pdfReader

    def read_pdf(self, pdfReader):
        metadata = self.funcs.read_meta(pdfReader, self.filepath)
        if metadata is None or type(metadata) == str and (metadata.endswith("could not be found.") or metadata.startswith("An unexpected error occured: ")):
            popupInfo = PopupInfo(metadata)
            return None
        else:
            labels = ["Title: ", "Author: ", "Subject: ", "Created on: ", "Changed on: ", "Creator: ", "PDF-Program: "]
            
            output = ""
            for i in range(len(metadata)):
                output = output + labels[i] + metadata[i] + "<br><br>" # <br> because '\n' does not work :P

            return output

    def add_layout(self, output):
        # add widgets
        self.gobackButton = QPushButton("  <  ")
        self.gobackButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.gobackButton.clicked.connect(self.switch_to_menu)

        infoLabel = QLabel(f"Metadata of: \"{os.path.basename(self.filepath)}\"")

        field = QTextEdit(output)
        field.setReadOnly(True)

        # add layouts
        layout = QVBoxLayout()
        
        # add widgets to layouts
        layout.addWidget(self.gobackButton)
        layout.addWidget(infoLabel)
        layout.addWidget(field)

        self.setLayout(layout)
        self.setStyleSheet("""
            QPushButton{
                background-color: #357ABD;
                color: #FFFFFF;
                border: 2px solid #2C6BC4;
                border-radius: 5px;
                padding: 3px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover{
                background-color: #2C6BC4;
            }

            QPushButton:pressed{
                background-color: #1A4A81;
            }

            QLabel{
                color: #FFFFFF;
                font-size: 15px;
                font-family: Arial;
                margin-top: 20px;
            }

            QTextEdit{
                color: #FFFFFF;
                font-size: 15px;
                font-family: Arial;
                padding: 17px;
                border: none
            }
        """)