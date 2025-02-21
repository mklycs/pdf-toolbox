from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QFileDialog
from views.view_menu import ViewMenu
from views.view_merge_pdfs import MergeWindow
from views.view_metadata_input import ViewMetadataInput
from views.view_metadata_display import ViewMetadataDisplay
from views.view_enter_password import ViewEnterPassword  

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF-Toolbox")
        self.setGeometry(100, 100, 700, 500)
        self.setMinimumSize(700, 500)

        self.mainLayout = QVBoxLayout()

        def switch_to_menu():
            self.currentWidget.deleteLater()
            self.currentWidget = ViewMenu(switch_to_merging, switch_to_display_metadata, switch_to_input_metadata, switch_to_add_password_to_pdf)
            self.mainLayout.addWidget(self.currentWidget)
            return

        def switch_to_merging():
            self.currentWidget.deleteLater()
            self.currentWidget = MergeWindow(switch_to_menu)

            amount = self.currentWidget.process_files()
            if amount < 1:
                switch_to_menu()
                return

            self.currentWidget.add_layout()
            self.mainLayout.addWidget(self.currentWidget)

        def switch_to_display_metadata():
            file, _ = QFileDialog.getOpenFileName(self, "Choose PDF", "", "(*.pdf)")
            if type(file) == str and len(file) < 2: # so if you choose no file with "getOpenFileName" then file is an \n or smth and saying if file == \n then it does not work
                return

            self.currentWidget.deleteLater()
            self.currentWidget = ViewMetadataDisplay(switch_to_menu, file)
            
            pdfReader = self.currentWidget.open_pdf()
            if pdfReader is None:
                switch_to_menu()
                return

            output = self.currentWidget.read_pdf(pdfReader)
            if output is None:
                switch_to_menu()
                return

            self.currentWidget.add_layout(output)
            self.mainLayout.addWidget(self.currentWidget)

        def switch_to_input_metadata():
            file, _ = QFileDialog.getOpenFileName(self, "Choose PDF", "", "(*.pdf)")
            if type(file) == str and len(file) < 2: # so if you choose no file with "getOpenFileName" then file is an \n or smth and saying if file == \n then it does not work
                return

            self.currentWidget.deleteLater()
            self.currentWidget = ViewMetadataInput(switch_to_menu, file)
            success = self.currentWidget.open_pdf()

            if success is None:
                switch_to_menu()
                return

            self.currentWidget.add_layout()
            self.mainLayout.addWidget(self.currentWidget)

        def switch_to_add_password_to_pdf():
            file, _ = QFileDialog.getOpenFileName(self, "Choose PDF", "", "(*.pdf)")
            if type(file) == str and len(file) < 2: # so if you choose no file with "getOpenFileName" then file is an \n or smth and saying if file == \n then it does not work
                return

            self.currentWidget.deleteLater()
            self.currentWidget = ViewEnterPassword(switch_to_menu, file)
            success = self.currentWidget.open_pdf()

            if success is None:
                switch_to_menu()
                return

            self.currentWidget.add_layout()
            self.mainLayout.addWidget(self.currentWidget)

        self.currentWidget = ViewMenu(switch_to_merging, switch_to_display_metadata, switch_to_input_metadata, switch_to_add_password_to_pdf)
        self.mainLayout.addWidget(self.currentWidget)
        self.setLayout(self.mainLayout)
        self.setStyleSheet("""
            QWidget{
                background-color: #2a2b2b;
            }
        """)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()