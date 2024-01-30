import time
import pyperclip
import os
import re
import threading
from openpyxl import Workbook, load_workbook
from datetime import datetime

# Global variables to control the execution and data sharing between threads
running = True
wb = Workbook()
ws = wb.active

def is_email(s):
    return '@' in s and '.' in s

def is_linkedin(s):
    return 'linkedin.com' in s

def is_phone_number(s):
    pattern = re.compile(r'\+\d{1,3}\s\d{3}-\d{3}-\d{4}')
    return pattern.match(s)

def write_to_excel(linkedin, email, phone_number):
    global ws
    ws.append([linkedin, email, phone_number])

def monitor_clipboard():
    global running, wb, ws

    ws.append(['LinkedIn', 'Email', 'Phone Number'])

    temp_email = ''
    temp_phone_number = ''
    last_clipboard_content = ""
    
    while running:
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != last_clipboard_content:
            if is_linkedin(current_clipboard_content):
                write_to_excel(current_clipboard_content, temp_email, temp_phone_number)
                temp_email = ''
                temp_phone_number = ''
            elif is_email(current_clipboard_content):
                temp_email = current_clipboard_content
            elif is_phone_number(current_clipboard_content):
                temp_phone_number = current_clipboard_content

            last_clipboard_content = current_clipboard_content
        
        time.sleep(0.5)

def main():
    global running, wb

    # Start clipboard monitoring in a separate thread
    thread = threading.Thread(target=monitor_clipboard)
    thread.start()

    print("Press K to quit.")
    while True:
        if input() == 'K':
            running = False
            break

    thread.join()  # Wait for the clipboard monitoring thread to finish

    # Ask for the custom filename
    custom_filename = input("What would you like to name the file? ") + '.xlsx'
    wb.save(custom_filename)
    print(f"File saved as {custom_filename}")

if __name__ == "__main__":
    main()
