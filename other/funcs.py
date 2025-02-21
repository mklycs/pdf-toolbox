from popups.popup_enter_password import PopupEnterPassword
from PySide6.QtWidgets import QDialog
from pypdf.generic import NameObject
import pypdf
import os

class Funcs():
    def __init__(self):
        pass
        
    def check_if_protected(self, filepath):
        with open(filepath, "rb") as file:                     
            reader = pypdf.PdfReader(filepath)
            if reader.is_encrypted:
                try:
                    p = PopupEnterPassword(filepath)
                    if p.exec_() == QDialog.Accepted:
                        password = p.get_password()
                    if not reader.decrypt(password):
                        raise ValueError("Wrong password. Access denied.")
                except Exception as exception:
                    return False
            return reader
    
    def save_pdf_file(self, writer, inputPath, outputPath):
        if outputPath == inputPath:                    # in other words to overwrite
            tempPath = inputPath + ".tmp"             
            with open(tempPath, "wb") as outputFile:   # creates a temporary file
                writer.write(outputFile)               # writes content of old file with new metadata into temporary file
                os.replace(tempPath, inputPath)        # replaces content of old file with content of temp file including metadata (so the the oldfile has the same old name and extension but with old content and new metadata) additionally os.replace removes/deletes the .tmp file
        else:
            with open(outputPath, "wb") as outputFile: # creates new same file with new metadata
                writer.write(outputFile)

    def merge_pdfs(self, files, outputPath): # files is a list in form of [[filepath, reader, int(beginning), int(end), maxPages], [filepath, reader, int(beginning), int(end), maxPages]]
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
                    self.save_pdf_file(writer, outputPath, outputPath)
                    return

            self.save_pdf_file(writer, "no overwrite", outputPath)

        except FileNotFoundError: return "The file(s) could not be found."
        except Exception as exception: return f"An unexpected error occured: {exception}"

    def protect_pdf(self, reader, filepath, password):
        if not reader: # "if reader is encrypted"
            return

        try:
            writer = pypdf.PdfWriter()
            
            for page in range(len(reader.pages)):
                writer.add_page(reader.pages[page])

            metadata = reader.metadata
            
            status = f"Removed password from \"{os.path.basename(filepath)}\"."
            if type(password) == str and len(password) > 0:
                writer.encrypt(user_password=password, use_128bit=True)
                status = f"Protection complete for \"{os.path.basename(filepath)}\"."

            if metadata:
                writer.add_metadata(metadata)
            
            with open(filepath, "wb") as outputFile:
                writer.write(outputFile)

            return status
        
        except FileNotFoundError: return f"The file \"{filepath}\" could not be found."
        except Exception as exception: return f"An unexpected error occured: {exception}"

    def read_meta(self, reader, filepath):
        if not reader: # "if reader is encrypted"
            return

        try:
            metadata = reader.metadata

            title = metadata.get("/Title", "Unknown")                
            author = metadata.get("/Author", "Unknown")
            subject = metadata.get("/Subject", "Unknown")
            creation_date = metadata.get("/CreationDate", "Unknown")
            mod_date = metadata.get("/ModDate", "Unknown")
            creator = metadata.get("/Creator", "Unknown")
            producer = metadata.get("/Producer", "Unknown")

            return [title, author, subject, creation_date, mod_date, creator, producer]

        except FileNotFoundError: return f"The file \"{filepath}\" could not be found."
        except Exception as exception: return f"An unexpected error occured: {exception}"

    def write_meta(self, reader, inputPath, outputPath, metadata):
        if not reader: # "if reader is encrypted"
            return

        try:    
            writer = pypdf.PdfWriter()

            for page_num in range(len(reader.pages)):     
                page = reader.pages[page_num]               
                writer.add_page(page) 

            if metadata == {}:                                                      
                writer.add_metadata({})                                      
            else:
                metaDict = {                                                       
                    NameObject("/Title"): metadata.get("/Title", ""),               
                    NameObject("/Author"): metadata.get("/Author", ""),
                    NameObject("/Subject"): metadata.get("/Subject", ""),
                    NameObject("/CreationDate"): metadata.get("/CreationDate", ""),
                    NameObject("/ModDate"): metadata.get("/ModDate", ""),
                    NameObject("/Creator"): metadata.get("/Creator", ""),
                    NameObject("/Producer"): metadata.get("/Producer", "")
                }
                writer.add_metadata(metaDict)

            self.save_pdf_file(writer, inputPath, outputPath)

        except FileNotFoundError: return f"The file \"{inputPath}\" could not be found."
        except Exception as exception: return f"An unexpected error occured: {exception}"