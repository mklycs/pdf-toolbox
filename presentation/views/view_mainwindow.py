from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PySide6.QtGui import QIcon
from presentation.views.view_merge_pdfs import MergeWindow
from presentation.views.view_show_pdf import ShowPDFdocument
from presentation.views.view_metadata_input import ViewMetadataInput

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./presentation/icons/pdf-toolbox.png"))
        self.setWindowTitle("PDF-Toolbox")
        self.setGeometry(100, 100, 700, 450)
        self.setMinimumSize(700, 450)
        self.generate_view()

    def generate_view(self)->bool:
        self.create_widgets()
        self.adjust_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.set_main_layout()
        return True

    def create_widgets(self)->None:
        self.centralWidget = QWidget()
        self.currentWidget = QTabWidget(self)

    def adjust_widgets(self)->None:
        self.currentWidget.addTab(MergeWindow(), "Merge PDFs")
        self.currentWidget.addTab(ShowPDFdocument(), "Open PDF(1)")
        self.currentWidget.addTab(ShowPDFdocument(), "Open PDF(2)")
        self.currentWidget.addTab(ViewMetadataInput(), "Change Metadata of PDF")

    def create_layouts(self)->None:
        self.mainLayout = QVBoxLayout(self.centralWidget)

    def add_widgets_to_layouts(self)->None:
        self.mainLayout.addWidget(self.currentWidget)

    def set_main_layout(self)->None:
        self.setCentralWidget(self.centralWidget)
        self.mainLayout.addWidget(self.currentWidget)
    
    def switch_to_(self, newWidget)->None:
        self.mainLayout.removeWidget(self.currentWidget)
        self.currentWidget.setParent(None) # removes the widget from central widget but does not delete it from memory
        self.currentWidget = newWidget
        self.currentWidget.generate_view()
        self.mainLayout.addWidget(self.currentWidget)

    def load_stylesheet(self, path: str) -> str:
        with open(path, "r") as styleSheet:
            return styleSheet.read()