import PyPDF2, os
from PyPDF2.generic import NameObject
from getpass import getpass

def protect_pdf(file_path):
    try:
        pdf_reader = PyPDF2.PdfReader(file_path)

        if pdf_reader.is_encrypted:
            existing_password = input("The file is currently encrypted. Enter the existing password to decrypt: ")
            try:
                pdf_reader.decrypt(existing_password)
            except Exception as exception:
                print("Failed to decrypt the file with the provided password: {}".format(exception))
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

def checkifEncrypted(reader):
    if reader.is_encrypted:
        try:
            existing_password = getpass("The file is currently encrypted. Enter the existing password to decrypt: ")
            if not reader.decrypt(existing_password):
                raise ValueError("Falsches Passwort. Zugriff verweigert.")
        except Exception as exception:
            print("Failed to decrypt the file with the provided password: {}".format(exception))
            return False
    return True

def read_meta(input_path):
    try:
        with open(input_path, "rb") as file:                     
            reader = PyPDF2.PdfReader(file)                      
            if not checkifEncrypted(reader):
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
            if not checkifEncrypted(reader):
                return
            writer = PyPDF2.PdfFileWriter()               

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
            
            if output_path == None: # in other words to not overwrite
                temp_path = input_path + ".tmp"             
                with open(temp_path, "wb") as output_file:   # creates a temporary file
                    writer.write(output_file)                # writes content of old file with new metadata into temporary file
                    os.replace(temp_path, input_path)        # replaces content of old file with content of temp file including metadata (so the the oldfile has the same old name and extension but with old content and new metadata) additionally os.replace removes/deletes the .tmp file
                while True:
                    Yn = input("Updated metadata successfully.\nNote: The updated PDF is not protected with a password anymore. Do you want to add a password to it? (Y/n): ")
                    if Yn == "Y": 
                        protect_pdf(input_path)
                        return
                    elif Yn == "n": return
                    else: print("Invalid input.")
            else:
                with open(output_path, "wb") as output_file: # creates new same file with new metadata
                    writer.write(output_file)
                while True:
                    Yn = input("Created new PDF with new metadata.\nNote: New PDF is not protected with a password. Do you want to add a password to it? (Y/n): ")
                    if Yn == "Y": 
                        protect_pdf(output_path)
                        return
                    elif Yn == "n": return
                    else: print("Invalid input.")

    except FileNotFoundError: print("The file \"{}\" could not be found.".format(input_path))
    except Exception as exception: print("An unexpected error occured: {}".format(exception))

def main():
    while(True):
        try:
            choice = int(input("\nChoose an option.\n1. Display metadata of PDF document\n2. Create new PDF document with diffrent metadata\n3. Overwrite metadata of PDF document\n4. Add password to PDF document\n0. Exit\nChoice: "))
            if choice == 0: return
            input_pdf = input("Enter the file path of the PDF file: ")
        except ValueError:
            return
        if choice == 1: 
            read_meta(input_pdf)
        elif choice == 2:
            output_pdf = input("Enter the file path of the output PDF file: ")
            write_meta(input_pdf, output_pdf)
        elif choice == 3:
            write_meta(input_pdf, None)
        elif choice == 4:
            protect_pdf(input_pdf)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
