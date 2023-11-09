import re
from bs4 import BeautifulSoup
import base64
import html

def get_plain_text_from_html(html_content):
    """
    Use BeautifulSoup to convert HTML content to plain text.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Use some heuristics to remove script, style, head, title, etc.
    for script_or_style in soup(['script', 'style', 'head', 'title']):
        script_or_style.extract()
    
    # Get text and decode HTML entities
    text = soup.get_text(separator='\n')
    text = html.unescape(text)
    
    # Regular expression to find URLs
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+|[^\s<>"]+\.[^\s<>"]{2,}'
    text = re.sub(url_pattern, '', text, flags=re.IGNORECASE)

    # Further processing to clean up the text
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
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

def extract_job_info(text):
    # Regular expressions for company name, city and pay range
    company_pattern = r'\n(.*?)\n- [A-Za-z]+, [A-Z]{2}'
    city_pattern = r'- ([A-Za-z]+), ([A-Z]{2})'
    pay_pattern = r'\$(\d+(?:,\d+)?(?: - \$\d+(?:,\d+)?)?) (a day|an hour|a week)'

    companies = re.findall(company_pattern, text)
    cities = re.findall(city_pattern, text)
    pays = re.findall(pay_pattern, text)

    # Combine the information
    job_listings = []
    for idx, company in enumerate(companies):
        city = f"{cities[idx][0]}, {cities[idx][1]}" if idx < len(cities) else "N/A"
        pay = " - ".join(pays[idx]) if idx < len(pays) else "N/A"
        job_listings.append((company, city, pay))

    return job_listings

job_info = extract_job_info(your_text_snippet)
