from PySide6.QtWidgets import QApplication
from presentation.views.view_mainwindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    stylesheet = window.load_stylesheet("presentation/custom/style.qss")
    window.show()
    app.setStyleSheet(stylesheet)
    app.exec()