from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QPushButton, QFrame, QLabel, QSpacerItem
from presentation.presenter.presenter_show_pdf import PresenterShowPDF
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
import os

# uncomment these if the gpu should have problems and displaying of the pdf should lead to crash of the program
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-gpu"
os.environ["QT_QUICK_BACKEND"] = "software"

class ShowPDFdocument(QWidget):
    def __init__(self, ):
        super().__init__()
        self.presenter = PresenterShowPDF(self)
        self.generate_view()

    def generate_view(self)->None:
        self.create_widgets()
        self.adjust_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.set_main_layout()
        self.set_widget_tag_for_styleqss()
            
    def create_widgets(self)->None:
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.choosePDFbutton = QPushButton("Open PDF")
        self.mainBody = QWidget()
        self.noPDFselectedLabel = QLabel("Currently no PDF selected.")
        self.frameForWebview = QFrame()
        self.webview = QWebEngineView()
        
    def adjust_widgets(self)->None:
        self.choosePDFbutton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.choosePDFbutton.clicked.connect(self.presenter.open_pdf)

        self.noPDFselectedLabel.setAlignment(Qt.AlignCenter)

        self.webview.settings().setAttribute(self.webview.settings().WebAttribute.PluginsEnabled, True)
        self.webview.settings().setAttribute(self.webview.settings().WebAttribute.PdfViewerEnabled, True)

    def create_layouts(self)->None:
        self.layout = QVBoxLayout()
        self.topbarLayout = QHBoxLayout()
        self.mainContentLayout = QVBoxLayout()
        self.mainBodyLayout = QVBoxLayout()
        self.webviewLayout = QVBoxLayout()

    def add_widgets_to_layouts(self)->None:
        self.topbarLayout.addItem(self.spacer)
        self.topbarLayout.addWidget(self.choosePDFbutton)

        self.mainContentLayout.addWidget(self.noPDFselectedLabel)

        self.mainBody.setLayout(self.mainContentLayout)
        self.mainBodyLayout.addWidget(self.mainBody)

        self.webviewLayout.addWidget(self.webview)
        self.frameForWebview.setLayout(self.webviewLayout)

    def set_main_layout(self)->None:
        self.layout.addLayout(self.topbarLayout)
        self.layout.addLayout(self.mainBodyLayout)
        self.layout.addLayout(self.webviewLayout)
        self.setLayout(self.layout)

    def set_widget_tag_for_styleqss(self)->None:
        self.choosePDFbutton.setObjectName("choosePDFbutton")
        self.mainBody.setObjectName("mainBody")
        self.noPDFselectedLabel.setObjectName("infoLabel")
