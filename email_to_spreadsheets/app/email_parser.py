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

def parse_email_body(email_content):
    """
    This function will now directly handle the email content.
    Assumes email_content is a string that may contain both plain text and HTML.
    """
    combined_text = ""

    # Check for both plain text and HTML in the email
    if 'text/plain' in email_content:
        combined_text += email_content['text/plain'] + "\n"
    if 'text/html' in email_content:
        html_content = email_content['text/html']
        combined_text += get_plain_text_from_html(html_content) + "\n"

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

email_content_example = {
    "text/plain": "Example Company\n- New York, NY\n$50,000 a year",
    "text/html": "<html><body><p>Example HTML Content</p></body></html>"
}

# Using parse_email_body to get plain text from the email
parsed_email_body = parse_email_body(email_content_example)

# Extract job information from the parsed email body
job_info = extract_job_info(parsed_email_body)

print(job_info)
print(parse_email_body)