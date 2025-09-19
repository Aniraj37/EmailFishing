from api.filereader import read_csv_file, read_excel_file, read_email_file, segment_extraction
# --- library for csv file ---
import types
# --- library for excel file ---
import os
from openpyxl import Workbook 
import tempfile


# === function to create test email file / csv file ===
def create_mock_file(content, content_type):
    '''
    - Simulates a file-like object that supports .read()
    '''
    return types.SimpleNamespace(
        read=lambda: content.encode("utf-8"),
        content_type=content_type    
    )
 

# === Test cases for read_csv_file(setup_file) ===
def test_read_csv_file_with_valid_file():
    """
    - Reads csv files and returns data in dictionary format.
    """
    csv_content = "start,end,phrase,segment_type\nA,B,Hello,Text\nC,D,World,\n"
    setup_file = create_mock_file(csv_content, content_type="text/csv")
    result = read_csv_file(setup_file)
    assert result == [
        {"start": "A", "end": "B", "phrase": "Hello", "segment_type": "text"},
        {"start": "C", "end": "D", "phrase": "World", "segment_type": "html"},
    ]

def test_read_csv_file_with_less_than_3_column():
    """
    - checks if provided setup_file has limited columns
    - function should return empty list.
    """
    csv_content = "start,end\nX,Y\n"
    setup_file = create_mock_file(csv_content, content_type="text/csv")
    result = read_csv_file(setup_file)
    assert result == []

def test_read_csv_file_with_empty_data():
    """
    - Check if file is empty or not
    - Test case pass if empty
    """
    csv_content = ""
    setup_file = create_mock_file(csv_content, content_type="text/csv")
    result = read_csv_file(setup_file)
    assert result == []






# === function to create mock excel file ===
def create_excel_file(rows):
    """
    - used for creating mock excel file
    """
    temp_file = tempfile.NamedTemporaryFile(delete = False, suffix = ".xlsx")
    wb = Workbook()
    ws = wb.active

    # --- Add header ---
    ws.append(["start", "end", "phrase", "segment_type"])

    # --- Add data in the file ---
    for _ in rows:
        ws.append(_)
    wb.save(temp_file.name)
    temp_file.close()
    return temp_file.name

def test_read_excel_file_with_valid_data():
    """
    - tests the data extraction process of the function
    """
    rows = [
        ["A", "B", "Phrase1", "Text"],
        ["A1", None, "Phrase2", None],
        ["A2", "B2", "Phrase3", "HTML"],
    ]
    file_path = create_excel_file(rows)
    result = read_excel_file(file_path)
    os.unlink(file_path) # --- removes the created file ---
    assert result == [
        {"start": "A", "end":"B", "phrase": "Phrase1", "segment_type":"text"},
        {"start": "A1", "end":"", "phrase": "Phrase2", "segment_type":"html"},
        {"start": "A2", "end":"B2", "phrase": "Phrase3", "segment_type":"html"},
    ]


def test_read_excel_file_with_no_data():
    """
    - test functions can deal with empty file or not
    """
    rows = []
    file_path = create_excel_file(rows)
    result = read_excel_file(file_path)
    os.unlink(file_path) # --- removes the created file ---
    assert result == []



# === function to create mock excel file ===
def test_read_email_file_with_valid_data():
    """
    - tests the main mechanish of the function
    """
    email_content = "Subject: Test\n\nThis is the body."
    email_file=create_mock_file(email_content, content_type="message/rfc822")
    result = read_email_file(email_file)
    assert result == [
        (1, "Subject: Test"),
        (2, ""),
        (3, "This is the body.")
    ]


def test_read_email_file_with_wrong_file_type():
    """
    - checks correct file type is uploaded.
    """
    email_content = "Subject: Test\n\nThis is the body."
    email_file=create_mock_file(email_content, content_type="text/csv")
    result = read_email_file(email_file)
    assert result == None


def test_read_email_file_with_empty_data():
    """
    - checks if [] is returned when empty file is uploaded
    """
    email_content = ""
    email_file=create_mock_file(email_content, content_type="message/rfc822")
    result = read_email_file(email_file)
    assert result == []

# === Test Cases for segment_extraction() ===
def test_multi_segment_extraction():
    """
    - tests multi segment extraction process
    """
    email_lines = [
        (1, "<body>"), 
        (2,"Hello, this is a test email."),
        (3,"is it working"),
        (4,"</body>")
        ]
    rules = [{'start': '<body', 'end': '</body>', 'phrase': 'test', 'segment_type': 'html'}]
    result = segment_extraction(email_lines, rules)
    assert result == {
        'test': {
            'segment_lines': ['<body>', 'Hello, this is a test email.','is it working', '</body>'], 
            'start_line': 1, 
            'status': 'Segment_found', 
            'matched_segments': [{'line': 2, 'text': 'Hello, this is a test email.'}], 
            'total_count': 1
            }
        }

def test_single_segment_extraction():
    """
    - test single line segment is working correctly
    """
    email_lines = [
        (1,"Hello, this is a test email."),
        (2, "test_id: be12-3sd"), 
        ]
    rules = [{'start': 'test_id', 'end': '', 'phrase': 'be12-3sd', 'segment_type': 'single'}]
    result = segment_extraction(email_lines, rules)
    assert result == {
        'be12-3sd': {
            'segment_lines': ['test_id: be12-3sd'], 
            'start_line': 2, 
            'status': 'Segment_found', 
            'matched_segments': [{'line': 2, 'text': 'test_id: be12-3sd'}], 
            'total_count': 1
            }
        }

def test_segment_extraction_segment_not_matched():
    """
    - checks if any segment from the rules is found in email
    """
    email_lines = [
        (1, "<body>"), 
        (2,"Hello, this is a test email."),
        (3,"is it working"),
        (4,"</body>")
        ]
    rules = [{'start': 'test_id', 'end': '', 'phrase': 'be12-3sd', 'segment_type': 'single'}]
    result = segment_extraction(email_lines, rules)
    assert result == None



# === Executes all the test cases ===
if __name__ == "__main__":
    print("Executing Test Cases")
    # --- TestCases for read_csv_file() ---
    test_read_csv_file_with_valid_file()
    test_read_csv_file_with_less_than_3_column()
    test_read_csv_file_with_empty_data()

    # --- TestCases for read_excel_file() ---
    test_read_excel_file_with_valid_data()
    test_read_excel_file_with_no_data()

    # --- TestCases for read_email_file() ---
    test_read_email_file_with_valid_data()
    test_read_email_file_with_wrong_file_type()
    test_read_email_file_with_empty_data()

    # --- TestCases for segment_extractions ---
    test_multi_segment_extraction()
    test_single_segment_extraction()
    test_segment_extraction_segment_not_matched()
    print("All 11 test cases passed.")