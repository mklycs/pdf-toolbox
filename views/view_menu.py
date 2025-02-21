from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QSpacerItem
from PySide6.QtCore import Qt

class ViewMenu(QWidget):
    def __init__(self, switch_to_merging, switch_to_display_metadata, switch_to_input_metadata, switch_to_add_password_to_pdf):
        super().__init__()

        self.switch_to_merging = switch_to_merging
        self.switch_to_display_metadata = switch_to_display_metadata
        self.switch_to_input_metadata = switch_to_input_metadata
        self.switch_to_add_password_to_pdf = switch_to_add_password_to_pdf

        # add widgets       
        vSpacerAbove = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.buttonMergePDFs = QPushButton("Merge PDFs")
        self.buttonMergePDFs.setFixedHeight(50)
        self.buttonMergePDFs.setFixedWidth(300)
        self.buttonMergePDFs.clicked.connect(self.switch_to_merging)
        
        self.buttonDisplayMetadata = QPushButton("Display metadata of PDF")
        self.buttonDisplayMetadata.setFixedHeight(50)
        self.buttonDisplayMetadata.setFixedWidth(300)
        self.buttonDisplayMetadata.clicked.connect(self.switch_to_display_metadata)
        
        self.buttonOverwriteMetadata = QPushButton("Overwrite metadata of PDF")
        self.buttonOverwriteMetadata.setFixedHeight(50)
        self.buttonOverwriteMetadata.setFixedWidth(300)
        self.buttonOverwriteMetadata.clicked.connect(self.switch_to_input_metadata)
        
        self.buttonAddPassword = QPushButton("Add password to PDF")
        self.buttonAddPassword.setFixedHeight(50)
        self.buttonAddPassword.setFixedWidth(300)
        self.buttonAddPassword.clicked.connect(self.switch_to_add_password_to_pdf) 

        vSpacerBelow = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # add layouts
        self.layout = QVBoxLayout()

        # add widgets to layouts
        self.layout.addItem(vSpacerAbove)
        self.layout.addWidget(self.buttonMergePDFs, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.buttonDisplayMetadata, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.buttonOverwriteMetadata, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.buttonAddPassword, alignment=Qt.AlignCenter)
        self.layout.addItem(vSpacerBelow)

        # add layouts to main layout

        self.setLayout(self.layout)
        self.setStyleSheet("""
            QLabel{
                color: #FFFFFF;
                font-size: 17px;
                font-family: Arial;
                margin-bottom: 20px;
            }

            QPushButton{
                background-color: #357ABD;
                color: #FFFFFF;
                border: 2px solid #2C6BC4;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover{
                background-color: #2C6BC4;
            }

            QPushButton:pressed{
                background-color: #1A4A81;
            }
        """)