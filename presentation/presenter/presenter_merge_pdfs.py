from PySide6.QtWidgets import QFileDialog, QListWidgetItem, QLabel
from presentation.custom.listitem import ListItem
from presentation.popups.popup_info import PopupInfo
from business.model_pdf_funcs import ModelPdfFuncs

class PresenterMergePDFs:
    def __init__(self, view):
        self.pdfReaders = {} # in order to prevent entering the password to pdf where password has already been entered once
        self.view = view
        self.model:ModelPdfFuncs = ModelPdfFuncs()

    def switch_mainBody_to(self, mainBody)->None:
        oldWidget = self.view.mainBody.layout().itemAt(0).widget()     # get the currently shown widget
        self.view.mainContentLayout.removeWidget(oldWidget)            # remove it instead of deleting the widget
        oldWidget.hide()                                               # hide the removed but still visible widget
        self.view.mainContentLayout.addWidget(mainBody)                # add the new widget to mainBodyLayout 
        mainBody.show()                                                # make it visible
        
    def add_listItem(self, pages:int, pdf:str)->None:
        if type(self.view.mainBody.layout().itemAt(0).widget()) is QLabel: # to not remove widgets every time a PDF is added even though the listwidget is already set (it somehow works without this if statement but whatever)
            self.switch_mainBody_to(self.view.fileList)
        
        item = QListWidgetItem()
        listitem = ListItem(pages, pages, pdf, self.remove_pdf_from_list)
        item.setSizeHint(listitem.sizeHint())
        self.view.fileList.addItem(item)
        self.view.fileList.setItemWidget(item, listitem)
        self.view.mergeButton.setEnabled(True)

    def get_amount_pages_from(self, pdf)->int:
        reader = self.model.handle_password_protected(pdf)
        if reader != False:
            self.pdfReaders.update({pdf : reader})
            return int(len(reader.pages))
        else: 
            return 0
    
    def add_pdfs(self)->None:
        pdfs, _ = QFileDialog.getOpenFileNames(self.view, "Choose PDF(s)", "", "(*.pdf)")
        for pdf in pdfs:
            pages:int = self.get_amount_pages_from(pdf)
            if pages > 0:
                self.add_listItem(pages, pdf)
            else: 
                popupInfo = PopupInfo("Failed to open the file with the provided password.")
    
    def merge_pages(self)->None:
        outputPath, _ = QFileDialog.getSaveFileName(self.view, "Save PDF", "", "(*.pdf)")
        if len(outputPath) < 1:
            return

        if outputPath.endswith(".pdf") == False:
            outputPath = outputPath + ".pdf"

        pdfs = []
        for row in range(self.view.fileList.count()):
            item = self.view.fileList.item(row)                  
            listItemWidget = self.view.fileList.itemWidget(item)
            if isinstance(listItemWidget, ListItem):
                pdfs.append([
                    listItemWidget.filepath,
                    self.pdfReaders[listItemWidget.filepath],
                    int(listItemWidget.beginning.currentText()),
                    int(listItemWidget.end.currentText()),
                    listItemWidget.last
                ])

        status:str = self.model.merge(pdfs, outputPath)
        popupInfo = PopupInfo(status)
    
    def remove_pdf_from_list(self, filepath)->None:                # or "delete recursively all elements from the listitem"
        amountListItems:int = self.view.fileList.count()
        if amountListItems-1 < 1:
            self.view.mergeButton.setEnabled(False)
            self.switch_mainBody_to(self.view.noPDFsSelectedLabel) # switch back to the label if there are no pdfs in the filelist

        for index in range(amountListItems):
            item = self.view.fileList.item(index)                  # gets the QListWidgetItem
            listitem = self.view.fileList.itemWidget(item)         # gets the associated ListItem-Widget
            if listitem and listitem.filepath == filepath:
                self.view.fileList.takeItem(index)
                del index
                return