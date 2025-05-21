from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QSizePolicy, QSizePolicy, QSpacerItem
from presentation.presenter.presenter_metadata_input import PresenterMetadataInput
from PySide6.QtCore import Qt

class ViewMetadataInput(QWidget):
    def __init__(self):
        super().__init__()
        self.presenter = PresenterMetadataInput(self)
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
        self.choosePDFbutton = QPushButton("Choose PDF")
        
        self.infoLabel = QLabel()
        
        self.mainBody = QWidget()
        self.noPDFselectedLabel = QLabel("Currently no PDF selected.")
        self.metadataForm = QWidget()
        
        self.inputTitle = QLineEdit()
        self.inputAuthor = QLineEdit()
        self.inputSubject = QLineEdit()
        self.inputCreationDate = QLineEdit()
        self.inputModDate = QLineEdit()
        self.inputCreator = QLineEdit()
        self.inputProducer = QLineEdit()
        self.inputPassword = QLineEdit()

        self.hSpacerRight = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.submitButton = QPushButton("Change")
        self.hSpacerLeft = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

    def adjust_widgets(self)->None:
        self.choosePDFbutton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.choosePDFbutton.clicked.connect(self.presenter.open_pdf)

        self.infoLabel.hide()

        self.vSpacerTop = QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.noPDFselectedLabel.setAlignment(Qt.AlignCenter)
        self.vSpacerBottom = QSpacerItem(0, 25, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.inputTitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputAuthor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputSubject.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputCreationDate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputModDate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputCreator.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputProducer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.inputPassword.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.inputPassword.setEchoMode(QLineEdit.Password)
        self.inputPassword.setPlaceholderText("Enter a password to protect the PDF:           (leaving this empty will remove the current password)")

        self.submitButton.clicked.connect(self.presenter.submit)
        self.submitButton.setFixedWidth(200)
        self.submitButton.setEnabled(False)

    def create_layouts(self)->None:
        self.layout = QVBoxLayout()
        self.topbarLayout = QHBoxLayout()
        self.mainContentLayout = QVBoxLayout()
        self.mainBodyLayout = QVBoxLayout()
        self.metadataFormLayout = QVBoxLayout()
        self.submitButtonLayout = QHBoxLayout()

    def add_widgets_to_layouts(self)->None:
        self.topbarLayout.addItem(self.spacer)
        self.topbarLayout.addWidget(self.choosePDFbutton)

        self.mainBodyLayout.addWidget(self.infoLabel)
        self.metadataFormLayout.addItem(self.vSpacerTop)
        self.metadataFormLayout.addWidget(self.inputTitle)
        self.metadataFormLayout.addWidget(self.inputAuthor)
        self.metadataFormLayout.addWidget(self.inputSubject)
        self.metadataFormLayout.addWidget(self.inputCreationDate)
        self.metadataFormLayout.addWidget(self.inputModDate)
        self.metadataFormLayout.addWidget(self.inputCreator)
        self.metadataFormLayout.addWidget(self.inputProducer)
        self.metadataFormLayout.addWidget(self.inputPassword)
        self.metadataFormLayout.addItem(self.vSpacerBottom)
        self.metadataForm.setLayout(self.metadataFormLayout)
        
        self.mainContentLayout.addWidget(self.noPDFselectedLabel)

        self.mainBody.setLayout(self.mainContentLayout)
        self.mainBodyLayout.addWidget(self.mainBody)
        
        self.submitButtonLayout.addItem(self.hSpacerRight)
        self.submitButtonLayout.addWidget(self.submitButton)
        self.submitButtonLayout.addItem(self.hSpacerLeft)

    def set_main_layout(self)->None:
        self.layout.addLayout(self.topbarLayout)
        self.layout.addLayout(self.mainBodyLayout)
        self.layout.addLayout(self.submitButtonLayout)
        self.setLayout(self.layout)

    def set_widget_tag_for_styleqss(self)->None:
        self.choosePDFbutton.setObjectName("choosePDFbutton")
        self.mainBody.setObjectName("mainBody")
        self.noPDFselectedLabel.setObjectName("infoLabel")
        self.infoLabel.setObjectName("infoLabel")
        self.inputTitle.setObjectName("modifyMeta")
        self.inputAuthor.setObjectName("modifyMeta")
        self.inputSubject.setObjectName("modifyMeta")
        self.inputCreationDate.setObjectName("modifyMeta")
        self.inputModDate.setObjectName("modifyMeta")
        self.inputCreator.setObjectName("modifyMeta")
        self.inputProducer.setObjectName("modifyMeta")
        self.inputPassword.setObjectName("modifyMeta")
        self.submitButton.setObjectName("mainButton")

    def get_new_metadata(self)->dict:
        return {
            "/Title": self.inputTitle.text(),
            "/Author": self.inputAuthor.text(),
            "/Subject": self.inputSubject.text(),
            "/CreationDate": self.inputCreationDate.text(),
            "/ModDate": self.inputModDate.text(),
            "/Creator": self.inputCreator.text(),
            "/Producer": self.inputProducer.text(),
            "Password": self.inputPassword.text()
        }