import PyPDF2, os
from PyPDF2.generic import NameObject
from getpass import getpass

def checkifProtected(reader, file_path):
    if reader.is_encrypted:
        try:
            existing_password = getpass("The file \"{}\" is currently encrypted. Enter the existing password to decrypt: ".format(file_path))
            if not reader.decrypt(existing_password):
                raise ValueError("Wrong password. Access denied.")
        except Exception as exception:
            print("Failed to decrypt the file with the provided password: {}".format(exception))
            return False
    return reader

def savePDFFile(writer, input_path, output_path, msg1, msg2):
    if output_path == input_path:                    # in other words to overwrite
        temp_path = input_path + ".tmp"             
        with open(temp_path, "wb") as output_file:   # creates a temporary file
            writer.write(output_file)                # writes content of old file with new metadata into temporary file
            os.replace(temp_path, input_path)        # replaces content of old file with content of temp file including metadata (so the the oldfile has the same old name and extension but with old content and new metadata) additionally os.replace removes/deletes the .tmp file
        while True:
            Yn = input(msg1)
            if Yn == "Y": 
                protect_pdf(input_path)
                return
            elif Yn == "n": return
            else: print("Invalid input.")
    else:
        with open(output_path, "wb") as output_file: # creates new same file with new metadata
            writer.write(output_file)
        while True:
            Yn = input(msg2)
            if Yn == "Y": 
                protect_pdf(output_path)
                return
            elif Yn == "n": return
            else: print("Invalid input.")

def merge_pdf():
    try:
        files = input("\nEnter the filepaths of the PDF documents you want to merge.\n(Note: the order of the files is important and make sure toseperate the filepaths with a whitespace (\" \")): ").split(" ")
        filepages = []
        pdf_writer = PyPDF2.PdfWriter() 
        for i,file in enumerate(files):
            pdf_reader = PyPDF2.PdfReader(file)
            pdf_reader = checkifProtected(pdf_reader, file)
            if pdf_reader == False:
                return
            
            pages = input("\nPlease enter the page range to merge from \"{}\".\nTo merge all pages, enter '0 0'. (For example, '1 5' to merge pages 1 through 5): ".format(file)).split(" ")
            pages[0] = int(pages[0])
            pages[1] = int(pages[1])

            if pages[0] == 0:
                for page in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page])
            else:
                for page in range(pages[0]-1, pages[1]):
                    pdf_writer.add_page(pdf_reader.pages[page])

        output_path = input("\nEnter the file path of the output PDF file: ")

        msg1 = "Updated PDF pages successfully.\nNote: The updated PDF is not protected with a password anymore. Do you want to add a password to it? (Y/n): " 
        msg2 = "Created new PDF with chosen PDF pages.\nNote: New PDF is not protected with a password. Do you want to add a password to it? (Y/n): "
        if output_path in files:
            savePDFFile(pdf_writer, output_path, output_path, msg1, msg2)
        else:
            savePDFFile(pdf_writer, "no overwrite", output_path, msg1, msg2)

    except FileNotFoundError: print("The file/s could not be found.")
    except Exception as exception: print("An unexpected error occured: {}".format(exception))

def protect_pdf(file_path):
    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        if not checkifProtected(pdf_reader, file_path):
            return

        pdf_writer = PyPDF2.PdfWriter()
        
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])

        password = getpass("Enter password: ")
        pdf_writer.encrypt(user_password=password, use_128bit=True)
        
        with open(file_path, "wb") as output_file:
            pdf_writer.write(output_file)

        print("Protection complete.")
    
    except FileNotFoundError: print("The file \"{}\" could not be found.".format(file_path))
    except Exception as exception: print("An unexpected error occured: {}".format(exception))

def read_meta(input_path):
    try:
        with open(input_path, "rb") as file:                     
            reader = PyPDF2.PdfReader(file)                      
            if not checkifProtected(reader, input_path):
                return
            metadata = reader.metadata                           

        title = metadata.get("/Title", "Unknown")                
        author = metadata.get("/Author", "Unknown")
        subject = metadata.get("/Subject", "Unknown")
        creation_date = metadata.get("/CreationDate", "Unknown")
        mod_date = metadata.get("/ModDate", "Unknown")
        creator = metadata.get("/Creator", "Unknown")
        producer = metadata.get("/Producer", "Unknown")
        print("Title: {}\nAuthor: {}\nSubject: {}\nCreated on: {}\nChanged on: {}\nCreator: {}\nPDF-Program: {}\n".format(title, author, subject, creation_date, mod_date, creator, producer))
    except FileNotFoundError: print("The file \"{}\" could not be found.".format(input_path))
    except Exception as exception: print("An unexpected error occured: {}".format(exception))

def input_info():
    print("\nSimply insert nothing and press enter in order to not enter something.")
    title = input("Enter new title: ")
    author = input("Enter new author: ")
    subject = input("Enter new subject: ")
    creation_date = input("Enter new date of file creation. (Format: YYYYMMDDHHMMSS): ")
    mod_date = input("Enter new date of file modification. (Format: YYYYMMDDHHMMSS): ")
    creator = input("Enter new creator: ")
    producer = input("Enter new production method of file: ")
    
    if not (title or author or subject or creation_date or mod_date or creator or producer):
        return {}

    creation_date = "D: " + creation_date
    mod_date = "D: " + mod_date
    
    metadata = {
        "/Title": title,
        "/Author": author,
        "/Subject": subject,
        "/CreationDate": creation_date,
        "/ModDate": mod_date,
        "/Creator": creator,
        "/Producer": producer
    }    

    return metadata

def write_meta(input_path, output_path):
    try:    
        with open(input_path, "rb") as file:              
            reader = PyPDF2.PdfReader(file)               
            if not checkifProtected(reader):
                return
            writer = PyPDF2.PdfWriter()             

            for page_num in range(len(reader.pages)):     
                page = reader.pages[page_num]               
                writer.add_page(page)   

            metadata = input_info()                  
            
            if metadata == {}:                                                      
                writer.add_metadata({})                                      
            else:
                meta_dict = {                                                       
                    NameObject("/Title"): metadata.get("/Title", ""),               
                    NameObject("/Author"): metadata.get("/Author", ""),
                    NameObject("/Subject"): metadata.get("/Subject", ""),
                    NameObject("/CreationDate"): metadata.get("/CreationDate", ""),
                    NameObject("/ModDate"): metadata.get("/ModDate", ""),
                    NameObject("/Creator"): metadata.get("/Creator", ""),
                    NameObject("/Producer"): metadata.get("/Producer", "")
                }
                writer.add_metadata(meta_dict)                                      
            
            msg1 = "Updated metadata successfully.\nNote: The updated PDF is not protected with a password anymore. Do you want to add a password to it? (Y/n): " 
            msg2 = "Created new PDF with new metadata.\nNote: New PDF is not protected with a password. Do you want to add a password to it? (Y/n): "
            savePDFFile(writer, input_path, output_path, msg1, msg2)

    except FileNotFoundError: print("The file \"{}\" could not be found.".format(input_path))
    except Exception as exception: print("An unexpected error occured: {}".format(exception))

def main():
    while(True):
        try:
            choice = int(input("\nChoose an option.\n1. Merge PDF pages\n2. Display metadata of PDF document\n3. Create new PDF document with diffrent metadata\n4. Overwrite metadata of PDF document\n5. Add password to PDF document\n0. Exit\nChoice: "))
            if choice == 0: return
        except ValueError:
            return
        if choice == 1:
            merge_pdf()
        elif choice == 2: 
            read_meta(input("Enter the file path of the PDF file: "))
        elif choice == 3:
            input_path = input("Enter the file path of the PDF file: ")
            output_path = input("Enter the file path of the output PDF file: ")
            write_meta(input_path, output_path)
        elif choice == 4:
            input_path = input("Enter the file path of the PDF file: ")
            write_meta(input_path, input_path)
        elif choice == 5:
            protect_pdf(input("Enter the file path of the PDF file: "))
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
