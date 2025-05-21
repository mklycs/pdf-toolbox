from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy, QComboBox, QPushButton
import os

class ListItem(QWidget):
    def __init__(self, first, last, filepath, remove_pdf_from_list):
        super().__init__()
        self.filepath = filepath
        self.remove_pdf_from_list = remove_pdf_from_list
        self.first = first
        self.last = last
        self.generate_widget()

    def generate_widget(self)->bool:
        self.create_layouts()
        self.create_widgets()
        self.add_widgets_to_layouts()
        self.set_main_layout()
        self.set_widget_tag_for_styleqss()
        return True

    def create_layouts(self)->None:
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.controlLayout = QHBoxLayout()

    def create_widgets(self)->None:
        self.label = QLabel(os.path.basename(self.filepath))
        self.label.setMaximumHeight(37)

        self.beginning = QComboBox(self)
        for i in range(1, self.first+1):
            self.beginning.addItem(str(i))

        self.beginning.setEditable(True)
        self.beginning.setFixedSize(57, 29)

        self.end = QComboBox(self)
        for i in range(1, self.last+1):
            self.end.addItem(str(i))
            
        self.end.setCurrentText(str(self.first))
        self.end.setEditable(True)
        self.end.setFixedSize(57, 29)

        self.removeButton = QPushButton(" x ")
        self.removeButton.clicked.connect(lambda: self.remove_pdf_from_list(self.filepath))
        self.removeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def add_widgets_to_layouts(self)->None:
        self.controlLayout.addWidget(self.beginning)
        self.controlLayout.addWidget(self.end)
        self.controlLayout.addWidget(self.removeButton)
        self.layout.addWidget(self.label)

    def set_main_layout(self)->None:
        self.layout.addLayout(self.controlLayout)
        self.setLayout(self.layout)

    def set_widget_tag_for_styleqss(self)->None:
        self.label.setObjectName("listItem")
        self.beginning.setObjectName("listItem")
        self.end.setObjectName("listItem")
        self.removeButton.setObjectName("listItem")