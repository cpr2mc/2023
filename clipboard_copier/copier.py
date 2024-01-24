import csv
import time
import pyperclip

def write_to_csv(content):
    with open('clipboard_history.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([content])

def main():
    last_clipboard_content = ""
    while True:
        current_clipboard_content = pyperclip.paste()
        if current_clipboard_content != last_clipboard_content:
            write_to_csv(current_clipboard_content)
            last_clipboard_content = current_clipboard_content
        time.sleep(.5)  # Wait for 1 second before checking again

if __name__ == "__main__":
    main()