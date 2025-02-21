from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QSpacerItem
from PySide6.QtCore import Qt
from custom.listitem import ListItem
from popups.popup_info import PopupInfo
from other.funcs import Funcs

class MergeWindow(QWidget):
    def __init__(self, switch_to_menu):
        super().__init__()

        self.switch_to_menu = switch_to_menu
        self.funcs = Funcs()
        self.pdfReader = {} # in order to prevent entering the password to pdf where password has already been entered once

    def get_amount_pdf_pages(self, filepath):
        reader = self.funcs.check_if_protected(filepath)
        if reader != False:
            self.pdfReader.update({filepath : reader})
            return len(reader.pages)
        else:
            return False
    
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Choose PDF(s)", "", "(*.pdf)")
        for file in files:
            amountPages = self.get_amount_pdf_pages(file)
            if type(amountPages) == int:
                item = QListWidgetItem()
                listitem = ListItem(amountPages, amountPages, file, self.remove_pdf_from_list) # os.path.basename(file)
                item.setSizeHint(listitem.sizeHint())
                self.fileList.addItem(item)
                self.fileList.setItemWidget(item, listitem)
            else: 
                popupInfo = PopupInfo("Failed to open the file with the provided password.")
    
    def merge_pages(self):
        outputPath, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "(*.pdf)")
        if len(outputPath) < 1:
            self.fileList.clear()
            self.switch_to_menu()
            return

        if outputPath.endswith(".pdf") == False:
            outputPath = outputPath + ".pdf"

        pdfsToMerge = []
        for row in range(self.fileList.count()):
            item = self.fileList.item(row)                  
            listItemWidget = self.fileList.itemWidget(item)
            if isinstance(listItemWidget, ListItem):
                filepath = listItemWidget.filepath
                beginning = listItemWidget.beginning.currentText()
                end = listItemWidget.end.currentText()
                maxPages = listItemWidget.maxPages
                reader = self.pdfReader[filepath]
                pdfsToMerge.append([filepath, reader, int(beginning), int(end), maxPages])
        
        self.funcs.merge_pdfs(pdfsToMerge, outputPath)

        popupInfo = QMessageBox()
        popupInfo.setMinimumSize(800, 800)
        popupInfo.setWindowTitle("Merge complete")
        popupInfo.setText("Completed merging PDF pages.")
        popupInfo.setIcon(QMessageBox.Information)
        popupInfo.setStandardButtons(QMessageBox.Ok)
        popupInfo.setDefaultButton(QMessageBox.Ok)

        ret = popupInfo.exec()

        self.fileList.clear()
        self.switch_to_menu()

    def process_files(self):
        self.fileList = QListWidget()
        self.fileList.setDragEnabled(True)
        self.fileList.setDropIndicatorShown(True)
        self.fileList.setDefaultDropAction(Qt.MoveAction)
        self.fileList.setDragDropMode(QListWidget.InternalMove)
        self.fileList.clear()

        self.add_files()
        
        return self.fileList.count()

    def remove_pdf_from_list(self, filepath):
        for index in range(self.fileList.count()):
            item = self.fileList.item(index)               # gets the QListWidgetItem
            listitem = self.fileList.itemWidget(item)      # gets the associated ListItem-Widget
            if listitem and listitem.filepath == filepath:
                self.fileList.takeItem(index)
                del index
                return

    def add_layout(self):
        # add widgets
        gobackButton = QPushButton("  <  ")
        gobackButton.setObjectName("cssButton")
        gobackButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        gobackButton.clicked.connect(self.switch_to_menu)

        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        moreFilesButton = QPushButton("Add files")
        moreFilesButton.setObjectName("cssButton")
        moreFilesButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        moreFilesButton.clicked.connect(self.add_files)

        hSpacerRight = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        mergeButton = QPushButton("Merge")
        mergeButton.setObjectName("cssButton")
        mergeButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mergeButton.clicked.connect(self.merge_pages)
        mergeButton.setFixedHeight(30)
        mergeButton.setFixedWidth(200)

        hSpacerLeft = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # add layouts
        layout = QVBoxLayout()
        horizontalTopLayout = QHBoxLayout()
        fileListLayout = QVBoxLayout()
        mergeButtonLayout = QHBoxLayout()

        # add widgets to layouts
        horizontalTopLayout.addWidget(gobackButton)
        horizontalTopLayout.addItem(spacer)
        horizontalTopLayout.addWidget(moreFilesButton)
        
        fileListLayout.addWidget(self.fileList)

        mergeButtonLayout.addItem(hSpacerRight)
        mergeButtonLayout.addWidget(mergeButton)
        mergeButtonLayout.addItem(hSpacerLeft)

        # add layouts to main layout
        layout.addLayout(horizontalTopLayout)
        layout.addLayout(fileListLayout)
        layout.addLayout(mergeButtonLayout)

        self.setLayout(layout)
        self.setStyleSheet("""
            QPushButton#cssButton{
                background-color: #357ABD;
                color: #FFFFFF;
                border: 2px solid #2C6BC4;
                border-radius: 5px;
                padding: 3px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton#cssButton:hover{
                background-color: #2C6BC4;
            }

            QPushButton#cssButton:pressed{
                background-color: #1A4A81;
            }

            QListWidget{
                border: None;
            }
        """)