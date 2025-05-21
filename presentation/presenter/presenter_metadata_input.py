from PySide6.QtWidgets import QFileDialog, QLabel
from presentation.popups.popup_info import PopupInfo
from business.model_pdf_funcs import ModelPdfFuncs
import os

class PresenterMetadataInput:
    def __init__(self, view):
        self.view = view
        self.model = ModelPdfFuncs()

    def switch_mainBody_to(self, mainBody)->None:
        if type(self.view.mainBody.layout().itemAt(0).widget()) is QLabel: # will only be executed once as it will never go back to "nothing selected"-label but whatever 
            oldWidget = self.view.mainBody.layout().itemAt(0).widget()     # get the currently shown widget
            self.view.mainContentLayout.removeWidget(oldWidget)            # remove it instead of deleting the widget
            oldWidget.hide()                                               # hide the removed but still visible widget
            self.view.mainContentLayout.addWidget(mainBody)                # add the new widget to mainBodyLayout 
            mainBody.show()                                                # make it visible

    def open_pdf(self)->bool:
        self.filepath, _ = QFileDialog.getOpenFileName(self.view, "Choose PDF", "", "(*.pdf)")
        self.pdfReader = self.model.open(self.filepath)
        if self.pdfReader != False:
            self.metadata:list = self.get_metadata()
            self.update_label(self.filepath)
            self.update_PlaceholderText()
            self.view.submitButton.setEnabled(True)
            self.switch_mainBody_to(self.view.metadataForm)
            return True
        
        return False

    def get_metadata(self)->list:
        metadata:list = self.model.read_meta(self.pdfReader)
        if metadata is None or type(metadata) == str and (metadata.endswith("could not be found.") or metadata.startswith("An unexpected error occured: ")):
            popupInfo = PopupInfo(metadata)
            return None
        else:
            return metadata

    def handle_input(self)->dict:
        metadata:dict = self.view.get_new_metadata()
        metadata = self.validate(metadata)
        return metadata

    def validate(self, inputdata:dict)->dict:
        for item in inputdata:
            if item == "Password":
                continue

            if not inputdata[item]:
                inputdata.update({item : "Unknown"})

        return inputdata
    
    def update_label(self, filePath:str)->None:
        self.view.infoLabel.setText(f"Changing metadata of: \"{os.path.basename(filePath)}\"")
        self.view.infoLabel.show()

    def update_PlaceholderText(self)->None:
        self.view.inputTitle.setPlaceholderText(f"Enter new title:                                              (Current title: {self.metadata[0]})")
        self.view.inputAuthor.setPlaceholderText(f"Enter new author:                                          (Current author: {self.metadata[1]})")
        self.view.inputSubject.setPlaceholderText(f"Enter new subject:                                         (Current subject: {self.metadata[2]})")
        self.view.inputCreationDate.setPlaceholderText(f"Enter new date of file creation:                     (Current file creation date: {self.metadata[3]})")
        self.view.inputModDate.setPlaceholderText(f"Enter new date of file modification:              (Current file modification date: {self.metadata[4]})")
        self.view.inputCreator.setPlaceholderText(f"Enter new creator:                                         (Current creator: {self.metadata[5]})")
        self.view.inputProducer.setPlaceholderText(f"Enter new production method of file:           (Current production method: {self.metadata[6]})")

    def clear_inputs(self)->None:
        self.view.inputTitle.clear()
        self.view.inputAuthor.clear()
        self.view.inputSubject.clear()
        self.view.inputCreationDate.clear()
        self.view.inputModDate.clear()
        self.view.inputCreator.clear()
        self.view.inputProducer.clear()
        self.view.inputPassword.clear()

    def submit(self)->None:
        metadata:dict = self.handle_input()
        outputPath, _ = QFileDialog.getSaveFileName(self.view, "Save PDF", "", "(*.pdf)")
        status:str = self.model.write_meta(self.pdfReader, self.filepath, outputPath, metadata)
        popupInfo = PopupInfo(status)
        
        if status.startswith("Successfully"):
            if outputPath == self.filepath:
                self.metadata = list(metadata.values())
                self.update_PlaceholderText()
            self.clear_inputs()