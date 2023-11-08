from bs4 import BeautifulSoup
import base64

def get_plain_text_from_html(html_content):
    """
    Use BeautifulSoup to convert HTML content to plain text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    # Use some heuristics to remove script, style, head, title, etc.
    for script_or_style in soup(['script', 'style', 'head', 'title']):
        script_or_style.extract()
    # Get text
    text = soup.get_text(separator='\n')
    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def parse_email_body(part):
    """
    Recursive function to parse the email body and extract all text from 'text/plain' parts.
    Convert 'text/html' parts to plain text using BeautifulSoup.
    """
    combined_text = ""

    mime_type = part.get("mimeType", "")
    part_body = part.get("body") or {}
    data = part_body.get("data")
    part_parts = part.get("parts", [])

    if mime_type == "text/plain" and data:
        # Decode text/plain part and append to combined_text
        text = base64.urlsafe_b64decode(data).decode("utf-8")
        combined_text += text + "\n"
    elif mime_type == "text/html" and data:
        # Decode text/html part, convert to plain text, and append to combined_text
        html = base64.urlsafe_b64decode(data).decode("utf-8")
        combined_text += get_plain_text_from_html(html) + "\n"
    elif part_parts:
        # If the part is multipart, recurse into it
        for subpart in part_parts:
            combined_text += parse_email_body(subpart)

    return combined_text
