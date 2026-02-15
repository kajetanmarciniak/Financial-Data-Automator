🚀 Universal Payroll & Data Automator

A professional Python-based automation tool designed to extract, clean, and aggregate financial data from multiple file formats including Excel (.xlsx, .xls), CSV, and PDF.

This solution eliminates manual data entry by providing a 100% offline, secure, and fast way to process scattered payroll or invoice information.
✨ Key Features

    Smart Column Detection: Uses intelligent keyword matching to find ID and Amount columns regardless of their names (supports English and Polish headers like User, Worker, Salary, Suma, etc.).

    Offline PDF Mining: Extracts structured text directly from PDFs using pdfplumber. No internet connection or expensive Cloud AI APIs required.

    Data Standardization: Automatically handles messy formatting:

        Converts commas to dots (e.g., 1200,50 -> 1200.50).

        Removes currency symbols and white spaces.

        Handles inconsistent naming conventions across different files.

    Privacy First: Processes all sensitive data locally on the user's machine. Ideal for GDPR-compliant workflows.

    Automatic Consolidation: Groups all found entries by User ID and generates a final, summed-up report in a clean Excel file.

🛠️ Tech Stack

    Python 3.x

    Pandas: For high-performance data manipulation and grouping.

    PDFPlumber: For precise, local PDF text extraction.

    OpenPyXL: The engine for generating professional .xlsx reports.

🚀 Installation & Setup
1. Requirements

Ensure you have Python installed. Then, install the necessary libraries:
Bash

pip install pandas pdfplumber openpyxl

2. Project Structure

The program automatically looks for a folder named PLIKI in the following locations:

    Same directory as the script

    Desktop

    OneDrive Desktop

3. Running the Tool

    Place your source files (Excels, PDFs, CSVs) inside the PLIKI folder.

    Run the script:
    Bash

    python main.py

    The consolidated report RAPORT_ZBIORCZY.xlsx will be generated inside the PLIKI folder.

💼 Commercial Value (Fiverr / Upwork)

This project serves as a "Commercial-Ready" automation tool. It can be easily compiled into a standalone .exe file using PyInstaller, allowing clients to use the software without ever touching a line of code or installing Python.

Example Use Case: An accountant receiving 50 different PDF invoices and 10 Excel sheets can merge them into one payment list in under 5 seconds.

Developed with ❤️ by PyFlow
