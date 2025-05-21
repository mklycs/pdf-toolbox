# PDF-Toolbox
This tool allows you to merge PDF pages, view and edit PDF metadata and protect PDF documents.

## Functions
1. **Merge PDFs**: Merge pages of PDF documents to an already existing PDF or a new document.
2. **Display metadata**: Displays the metadata of a PDF document.
3. **Overwrite metadata of a PDF**: Overwrites the metadata of an existing PDF file.
4. **Add password to PDF**: Adds a password to a PDF file to protect it.

## Prerequisites
- Python 3.x
    - Windows: [Download Python](https://www.python.org/downloads/)
    - Linux/macOS: Python is usually pre-installed. If not it can be installed with your systems package manager.

## Installing and running the Repository
### 1. Cloning the Repository:  
Open the terminal and run:  
```bash
git clone https://github.com/mklycs/pdf-toolbox.git
```
Alternatively, the ZIP file can be downloaded from the repository and extracted.

### 2. Navigating to the Project Folder:
```bash
cd pdf-toolbox
```

### 3. Creating a virtual environment
- on Linux/macOS:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
- on Windows:
    ```bash
    python -m venv venv
    source venv\Scripts\activate
    ```

### 4. Installing Dependencies
```bash
pip install -r requirements.txt
```
### 5. Running the Application:
```bash
python main.py
```

## Building an Executable (optional)
To build an executable the pyinstaller module can be used. It can be installed in the actively running virtual environment with:
```bash
pip install pyinstaller
```
After the pyinstaller module finished downloading the following command can be used to build the executable:
```bash
pyinstaller -F -w -i icon.ico main.py
```
Argument options:
- F ... adds everything to one file
- w ... removes terminal window
- i ... adds custom icon (so icon.ico will be the icon of this executable)
- main.py ... the file that will be made to an executable

After the build has finished two new folders can be found in the project folder: "build" and "dist". In "dist" will be the executable located, which can be moved anywhere and in "build" the temporary files which pyinstaller needs to build the executable and can be deleted.
