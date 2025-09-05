# import csv
# import re

# def read_setup_file(setup_path):
#     suspicious_phrases = []
#     with open(setup_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         for row in reader:
#             if len(row) < 3:
#                 continue
#             start, end, phrase = row[0].strip(), row[1].strip(), row[2].strip()
#             suspicious_phrases.append((start, end, phrase))
#     return suspicious_phrases

# def read_email_file(email_path):
#     with open(email_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#     return lines

# def extract_segment(lines, start_tag, end_tag):
#     start_idx, end_idx = None, None
#     for i, line in enumerate(lines):
#         if start_tag in line and start_idx is None:
#             start_idx = i
#         if end_tag in line and start_idx is not None:
#             end_idx = i
#             break
#     if start_idx is not None and end_idx is not None:
#         segment = ''.join(lines[start_idx:end_idx+1])
#         return segment, start_idx+1  # line numbers start at 1
#     return None, None

# def main():
#     setup_file = 'setup.csv '  # Change to your setup file path
#     email_file = 'email.eml'  # Change to your email file path

#     suspicious_phrases = read_setup_file(setup_file)
#     email_lines = read_email_file(email_file)

#     for start_tag, end_tag, phrase in suspicious_phrases:
#         segment, line_num = extract_segment(email_lines, start_tag, end_tag)
#         if segment:
#             print(f"Segment starting at line {line_num}:\n{segment}\n")
#             if re.search(re.escape(phrase), segment, re.IGNORECASE):
#                 print(f"FAIL: Suspicious phrase found: '{phrase}'\n")
#             else:
#                 print("PASS: No suspicious phrase found.\n")
#         else:
#             print(f"Segment '{start_tag}' to '{end_tag}' not found in email.\n")

# if __name__ == "__main__":
#     main()



import csv

def load_setup_rules(file_path):
    """
    Load setup rules from a CSV file.
    CSV format: start_segment, end_segment, suspicious_phrase
    Returns a list of dictionaries.
    """
    rules = []
    with open(file_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=["start", "end", "phrase"])
        for row in reader:
            rules.append({
                "start": row["start"].strip(),
                "end": row["end"].strip(),
                "phrase": row["phrase"].strip()
            })
    return rules


def load_email(file_path):
    """
    Load email file (.eml) into a list of lines with line numbers.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return list(enumerate(f.readlines(), start=1))


def extract_segment(email_lines, start_tag, end_tag):
    """
    Extract text between start_tag and end_tag.
    Returns the segment text and the line number where it starts.
    """
    inside_segment = False
    segment_lines = []
    start_line_num = None

    for line_num, line in email_lines:
        if start_tag in line and not inside_segment:
            inside_segment = True
            start_line_num = line_num
        if inside_segment:
            segment_lines.append(line)
        if end_tag in line and inside_segment:
            break

    return segment_lines, start_line_num


def search_suspicious(segment_lines, suspicious_phrase):
    """
    Search for suspicious_phrase in extracted segment.
    Returns True if found, False otherwise.
    """
    segment_text = " ".join(segment_lines).lower()
    return suspicious_phrase.lower() in segment_text


def main():
    setup_file = "setup.csv"   # Example: your setup file
    email_file = "email.eml"   # Example: your email file

    # Load rules and email
    rules = load_setup_rules(setup_file)
    email_lines = load_email(email_file)

    # Process each rule
    for rule in rules:
        segment, start_line = extract_segment(email_lines, rule["start"], rule["end"])
        if not segment:
            print(f"[INFO] Segment {rule['start']}..{rule['end']} not found in email.")
            continue

        print(f"\n--- Checking segment starting at line {start_line} ---")
        found = search_suspicious(segment, rule["phrase"])

        if found:
            print(f"[FAIL] Suspicious phrase '{rule['phrase']}' found in email segment!")
        else:
            print(f"[PASS] No suspicious phrase '{rule['phrase']}' found.")


if __name__ == "__main__":
    main()
