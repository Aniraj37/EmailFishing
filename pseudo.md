# PC1.0
# Auther: Aniraj
# Date: 09/09/2025
# Program: Spot the Phishing Email

# START
    # Define supported file types (CSV, Excel)
    # CREATE a database with model "EmailScan", "FailureEmail"
        # EmailScan: id, setup_file, email_file, uploaded_at
        # email (FK), phrase, start_line, segment_lines, matched_segments, total_count, created_at,
    
    # Define a FUNCTION read_setup_file(setup_file)
        # Reads csv or excel files
        # Return data in dictionary format
    
    # Define a FUNCTION read_email_file(email_file)
        # Reads .eml file
        # Return data in Nested list structure
    
    # Define a FUNCTION segment_extraction(email_line, rules)
        # Reads data from email_line, and rules
        # Process the  
    
    # Create FileReader API (Checks suspicious phrase) 
        # Ask user for setup_file & email_file
        # Call read_setup_file(setup_file)
            # returns setup_results
        # Call read_excel_file(excel_file)
            # returns email_results
        # call segment_extraction(setup_results, email_results)
            # IF no phrase found:
                # PRINT Pass
            # Else: 
                # PRINT Fail
                # Insert failed details in the database

    # Create FileReaderView API
        # Retrives data from the EmailScan, EmailFailure
        # PRINT result

    # Create FileByIDView API
        # Ask user for UUID
        # Filter the database by UUID and retrive data
        # PRINT result

# END
