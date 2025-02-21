from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QComboBox, QPushButton
import os

class ListItem(QWidget):
    def __init__(self, first, last, filepath, remove_pdf_from_list):
        super().__init__()

        self.filepath = filepath
        self.remove_pdf_from_list = remove_pdf_from_list
        self.maxPages = last

        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)

        label = QLabel(os.path.basename(self.filepath))
        label.setMaximumHeight(37)

        self.beginning = QComboBox(self)
        for i in range(1, first+1):
            self.beginning.addItem(str(i))

        self.beginning.setEditable(True)
        self.beginning.setFixedSize(57, 29)

        self.end = QComboBox(self)
        for i in range(1, self.maxPages+1):
            self.end.addItem(str(i))
            
        self.end.setCurrentText(str(first))
        self.end.setEditable(True)
        self.end.setFixedSize(57, 29)

        removeButton = QPushButton(" x ")
        removeButton.clicked.connect(lambda: self.remove_pdf_from_list(self.filepath))
        removeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.beginning)
        controlLayout.addWidget(self.end)
        controlLayout.addWidget(removeButton)

        layout.addWidget(label)
        layout.addLayout(controlLayout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QPushButton{
                background-color: #C94C4C;
                color: #FFFFFF;
                border: 2px solid #B03C3C;
                border-radius: 5px;
                padding: 3px;
                font-size: 16px;
                font-weight: bold;
                margin: 2px;
            }

            QPushButton:hover{
                background-color: #B03C3C;
            }

            QPushButton:pressed{
                background-color: #802B2B;
            }

            QScrollArea{
                border: none;
            }

            QLabel{
                color: #FFFFFF;
                font-size: 17px;
                font-family: Arial;
                border: none;
                border-bottom: 1px solid #3d3d3d;
            }

            QComboBox{
                color: #FFFFFF;
                border: 1px solid #357ABD;
                border-radius: 2px;
                font-size: 15px;
                padding: 5px;
            }

            QComboBox:hover{
                background-color: #757575;
            }
            
            QComboBox QAbstractItemView{
                selection-background-color: #757575;
                color: #FFFFFF;
            }
        """)
        