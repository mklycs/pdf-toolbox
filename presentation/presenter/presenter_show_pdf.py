from PySide6.QtWidgets import QFileDialog, QLabel
from PySide6.QtCore import QUrl
from presentation.popups.popup_info import PopupInfo
from business.model_pdf_funcs import ModelPdfFuncs
import os

class PresenterShowPDF:
    def __init__(self, view):
        self.view = view
        self.model = ModelPdfFuncs()

    def set_webview(self)->None:
        pdf_url = QUrl.fromLocalFile(os.path.abspath(self.filepath))
        pdf_url.setFragment("zoom=page-width")
        self.view.webview.setUrl(pdf_url)

    def switch_mainBody_to(self, mainBody)->None:
        if type(self.view.mainBody.layout().itemAt(0).widget()) is QLabel: # will only be executed once as it will never go back to "nothing selected"-label but whatever 
            oldWidget = self.view.mainBody.layout().itemAt(0).widget()     # get the currently shown widget
            self.view.mainContentLayout.removeWidget(oldWidget)            # remove it instead of deleting the widget
            oldWidget.hide()                                               # hide the removed but still visible widget
            self.view.mainContentLayout.addWidget(mainBody)                # add the new widget to mainBodyLayout 
            mainBody.show()                                                # make it visible

    def open_pdf(self)->bool:
        self.filepath, _ = QFileDialog.getOpenFileName(self.view, "Choose PDF", "", "(*.pdf)")
        if len(self.filepath) > 0:
            self.set_webview()
            self.switch_mainBody_to(self.view.frameForWebview)
            return True
        return False