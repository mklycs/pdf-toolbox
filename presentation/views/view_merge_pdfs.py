from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QListWidget, QSpacerItem, QLabel
from PySide6.QtCore import Qt
from presentation.presenter.presenter_merge_pdfs import PresenterMergePDFs

class MergeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.presenter = PresenterMergePDFs(self)
        self.generate_view()

    def generate_view(self)->bool:
        self.create_widgets()
        self.adjust_widgets()
        self.create_layouts()
        self.add_widgets_to_layouts()
        self.set_main_layout()
        self.set_widget_tag_for_styleqss()
        return True

    def create_widgets(self)->None:
        self.spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.moreFilesButton = QPushButton("Add PDF(s)")
        
        self.mainBody = QWidget()
        self.noPDFsSelectedLabel = QLabel("Currently no PDF(s) selected.")
        self.fileList = QListWidget()
        
        self.hSpacerRightButton = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.mergeButton = QPushButton("Merge")
        self.hSpacerLeftButton = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

    def adjust_widgets(self)->None:
        self.moreFilesButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.moreFilesButton.clicked.connect(self.presenter.add_pdfs)

        self.noPDFsSelectedLabel.setAlignment(Qt.AlignCenter)

        self.fileList.setDragEnabled(True)
        self.fileList.setDropIndicatorShown(True)
        self.fileList.setDefaultDropAction(Qt.MoveAction)
        self.fileList.setDragDropMode(QListWidget.InternalMove)
        self.fileList.clear()

        self.mergeButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.mergeButton.clicked.connect(self.presenter.merge_pages)
        self.mergeButton.setFixedWidth(200)
        self.mergeButton.setEnabled(False)

    def create_layouts(self)->None:
        self.layout = QVBoxLayout()
        self.topbarLayout = QHBoxLayout()
        self.mainContentLayout = QVBoxLayout()
        self.mainBodyLayout = QVBoxLayout()
        self.mergeButtonLayout = QHBoxLayout()

    def add_widgets_to_layouts(self)->None:
        self.topbarLayout.addItem(self.spacer)
        self.topbarLayout.addWidget(self.moreFilesButton)
        
        self.mainContentLayout.addWidget(self.noPDFsSelectedLabel)

        self.mainBody.setLayout(self.mainContentLayout)
        self.mainBodyLayout.addWidget(self.mainBody)

        self.mergeButtonLayout.addItem(self.hSpacerRightButton)
        self.mergeButtonLayout.addWidget(self.mergeButton)
        self.mergeButtonLayout.addItem(self.hSpacerLeftButton)

    def set_main_layout(self)->None:
        self.layout.addLayout(self.topbarLayout)
        self.layout.addLayout(self.mainBodyLayout)
        self.layout.addLayout(self.mergeButtonLayout)
        self.setLayout(self.layout)

    def set_widget_tag_for_styleqss(self)->None:
        self.moreFilesButton.setObjectName("choosePDFbutton")
        self.mainBody.setObjectName("mainBody")
        self.noPDFsSelectedLabel.setObjectName("infoLabel")
        self.mergeButton.setObjectName("mainButton")