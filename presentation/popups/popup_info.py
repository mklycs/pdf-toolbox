from PySide6.QtWidgets import QMessageBox

class PopupInfo(QMessageBox):
    def __init__(self, message):
        super().__init__()

        self.setMinimumSize(800, 800)

        if message is None:
            message = "Failed to open the file with the provided password."

        if message.startswith("Failed"):
            self.setWindowTitle("Error")
            self.setIcon(QMessageBox.Critical)
        elif message.startswith("The file"):
            self.setWindowTitle("Warning")
            self.setIcon(QMessageBox.Warning)
        elif message.startswith("An unexpected"):
            self.setWindowTitle("Error")
            self.setIcon(QMessageBox.Critical)
        else: # "Completed merging PDF pages."
            self.setWindowTitle("Information")
            self.setIcon(QMessageBox.Information)
        
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)

        ret = self.exec()