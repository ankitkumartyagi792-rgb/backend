import re

def extract_urls(text):
    """Extract URLs from text."""
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return url_pattern.findall(text)

def check_link_safety(urls):
    """Dummy check for link safety."""
    if not urls:
        return "Safe"
    # Basic check against dummy bad words in URL
    suspicious_phrases = ['pay', 'fake', 'secure', 'update', 'login', 'xyz', 'free']
    for url in urls:
        for phrase in suspicious_phrases:
            if phrase in url.lower():
                return "Malicious"
    return "Unknown/Suspicious"
