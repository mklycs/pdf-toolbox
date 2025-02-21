from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel

class PopupEnterPassword(QDialog):
    def __init__(self, filepath):
        super().__init__()
        self.setWindowTitle("PDF is protected")
        self.setMinimumSize(700, 200)

        layout = QVBoxLayout()

        label = QLabel(f"The file \"{filepath}\" is protected with a password.")
        layout.addWidget(label)

        self.inputfield = QLineEdit()
        self.inputfield.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.inputfield)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def get_password(self):
        return self.inputfield.text()