from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel

class PopupEnterPassword(QDialog):
    def __init__(self, filepath):
        super().__init__()
        self.setWindowTitle("PDF is protected")
        self.setMinimumSize(700, 200)
        self.filepath = filepath
        self.generate_view()

    def generate_view(self)->bool:
        self.create_layouts()
        self.create_widgets()
        self.adjust_widgets()
        self.add_widgets_to_layouts()
        self.set_main_layout()
        self.set_widget_tag_for_styleqss()
        return True

    def create_layouts(self)->None:
        self.layout = QVBoxLayout()

    def create_widgets(self)->None:
        self.label = QLabel(f"The file \"{self.filepath}\" is protected with a password.")
        self.inputfield = QLineEdit()
        self.okButton = QPushButton("OK")

    def adjust_widgets(self)->None:
        self.inputfield.setEchoMode(QLineEdit.Password)
        self.okButton.clicked.connect(self.accept)

    def add_widgets_to_layouts(self)->None:
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.inputfield)
        self.layout.addWidget(self.okButton)

    def set_main_layout(self)->None:
        self.setLayout(self.layout)

    def set_widget_tag_for_styleqss(self)->None:
        return

    def get_password(self)->str:
        if self.exec_() == QDialog.Accepted:
            return self.inputfield.text()
        return ""