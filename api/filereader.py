import csv, re
from openpyxl import load_workbook


EXTENTION_LIST = [
    "text/plain",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]


def read_setup_file(setup_file):
    """
    - Reads different types of files : txt, csv, xls
    - Loads rules from the file
    - returns a list of dictionaries
    """
    if setup_file.content_type not in EXTENTION_LIST:
        return None
    
    if setup_file.content_type =="text/plain":
        return read_text_file(setup_file)
    
    if setup_file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return read_excel_file(setup_file)
    

def read_csv_file(setup_file):
    """
    - Reads csv file and segrigates the text and appends to empty list in a dictionary format.
    - Remives the first row as it assumes it as a header.
    """
    suspicious_phrases = []
    decoded_file = setup_file.read().decode("utf-8").splitlines()
    file_content = csv.reader(decoded_file)

    next(file_content, None)

    for col in file_content:
        if len(col) >=3:
            suspicious_phrases.append({
                "start": col[0].strip(),
                "end": col[1].strip(),
                "phrases": [_.strip() for _ in re.split(r'[,,]', col[2]) if _.strip()],
                "segment_type": col[3].strip().lower() if len(col) >= 4 and col[3].strip() else "html"
            })

    return suspicious_phrases


def read_excel_file(setup_file):
    """
    - Reads excel file and segrigates the text and appends to empty list in a dictionary format.
    """
    suspicious_phrases = []
    work_book = load_workbook(setup_file, data_only=True)
    file_content = work_book.active

    for col in file_content.iter_rows(min_row = 2,values_only=True):
        if len(col) >= 3:    
            suspicious_phrases.append({
                    "start": col[0].strip(),
                    "end": col[1].strip() if col[1] else "",
                    "phrases": [_.strip() for _ in re.split(r'[,,]', col[2]) if _.strip()],
                    "segment_type": str(col[3]).strip().lower() if len(col) >= 4 and col[3] else "html" 
                })

    return suspicious_phrases
        

def read_email_file(email_file):
    """
    - reads email file (.eml) into a list of lines with the line numbers.
    """
    file_content=email_file.read().decode("utf-8", errors="ignore")
    lines = file_content.splitlines()
    return list(enumerate(lines, start=1))