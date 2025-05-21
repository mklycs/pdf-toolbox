from presentation.popups.popup_enter_password import PopupEnterPassword
from presentation.popups.popup_info import PopupInfo
from pypdf.generic import NameObject
import pypdf
import os

class ModelPdfFuncs:
    def __init__(self):
        pass

    def open(self, filepath:str):#->Union[pypdf._reader.PdfReader, bool]:
        if type(filepath) == str and len(filepath) < 2: # if no file is chosen then file is an \n or smth and saying if file == \n then it does not work :P
            return False

        pdfReader = self.handle_password_protected(filepath)
        if not pdfReader:
            popupInfo = PopupInfo("Failed to open the file with the provided password.")
            return False
        else:
            return pdfReader

    def handle_password_protected(self, filepath:str):#->Union[pypdf._reader.PdfReader, bool]:
        with open(filepath, "rb") as file:                     
            reader = pypdf.PdfReader(filepath)
            if reader.is_encrypted:
                password = PopupEnterPassword(filepath).get_password() # no way this works...
                if not reader.decrypt(password):
                    return False
            return reader

    def save_pdf_file(self, writer, inputPath:str, outputPath:str)->None:
        if outputPath == inputPath:                    # in other words to overwrite
            tempPath:str = inputPath + ".tmp"             
            with open(tempPath, "wb") as outputFile:   # creates a temporary file
                writer.write(outputFile)               # writes content of old file into temporary file
            os.replace(tempPath, inputPath)            # replaces content of old file with content of temp file including metadata (so the the oldfile has the same old name and extension but with old content and new metadata) additionally os.replace removes/deletes the .tmp file
        else:
            with open(outputPath, "wb") as outputFile: # creates new same file with new metadata
                writer.write(outputFile)

    def merge(self, files, outputPath:str)->str:   # files is a list in form of [[filepath, reader, int(beginning), int(end), maxPages], [filepath, reader, int(beginning), int(end), maxPages]]
        try:
            writer = pypdf.PdfWriter() 
            for f in files:                        # f[0] = filepath, f[1] = reader,  f[2] = beginning, f[3] = end, f[4] = maxPages
                beginning = f[2]
                end = f[3]
                maxPages = f[4]
                if (beginning - 1) < 0:            # if beginning is lower than 0 (it is out of index range)
                    beginning = 1 
                
                if end > maxPages or end < 1:      # if end is bigger than the maximum amount of pages or is out of index range
                    end = maxPages
                
                if beginning >= end:
                    beginning = end

                for i in range(beginning-1, end):
                    writer.add_page(f[1].pages[i])

            for f in files:
                if f[0] == outputPath:
                    self.save_pdf_file(writer, outputPath, outputPath) # this does not work on windows (will throw exception)
                    return "Completed merging PDF pages."

            self.save_pdf_file(writer, "no overwrite", outputPath)
            return "Completed merging PDF pages."

        except FileNotFoundError: return "The file(s) could not be found."
        except Exception as exception: return f"An unexpected error occured: {exception}"

    def read_meta(self, reader):#->Union[list, str]:
        if not reader: # "if reader is encrypted"
            return # return some string

        try:
            return [
                reader.metadata.get("/Title", "Unknown"), 
                reader.metadata.get("/Author", "Unknown"), 
                reader.metadata.get("/Subject", "Unknown"), 
                reader.metadata.get("/CreationDate", "Unknown"), 
                reader.metadata.get("/ModDate", "Unknown"), 
                reader.metadata.get("/Creator", "Unknown"), 
                reader.metadata.get("/Producer", "Unknown")
            ]

        except Exception as exception: return f"An unexpected error occured: {exception}"

    def write_meta(self, reader, inputPath:str, outputPath:str, metadata)->str:
        if not reader: # "if reader is encrypted"
            return # return some string

        try:    
            writer = pypdf.PdfWriter()

            for page_num in range(len(reader.pages)):     
                page = reader.pages[page_num]               
                writer.add_page(page) 

            if metadata == {}:                                                      
                writer.add_metadata({})                                      
            else:
                metaDict = {
                    NameObject("/Title"): metadata.get("/Title") or "Unknown",
                    NameObject("/Author"): metadata.get("/Author") or "Unknown",
                    NameObject("/Subject"): metadata.get("/Subject") or "Unknown",
                    NameObject("/CreationDate"): metadata.get("/CreationDate") or "Unknown",
                    NameObject("/ModDate"): metadata.get("/ModDate") or "Unknown",
                    NameObject("/Creator"): metadata.get("/Creator") or "Unknown",
                    NameObject("/Producer"): metadata.get("/Producer") or "Unknown"
                }
                writer.add_metadata(metaDict)

            # if a password is set, encrypt the PDF doc
            password:str = metadata['Password']
            if type(password) == str and len(password) > 0:
                writer.encrypt(user_password=password, use_128bit=True)

            self.save_pdf_file(writer, inputPath, outputPath)
            return f"Successfully changed metadata of: \"{os.path.basename(outputPath)}\"."

        except FileNotFoundError: return f"The file \"{inputPath}\" could not be found."
        except Exception as exception: return f"An unexpected error occured: {exception}"