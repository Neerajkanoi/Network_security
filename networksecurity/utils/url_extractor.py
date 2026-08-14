import pandas as pd
import urllib.parse
import re
import ipaddress

def extract_features(url: str) -> pd.DataFrame:
    """
    Extracts 30 features from a given URL to match the Phishing dataset schema.
    Returns a pandas DataFrame with exactly 1 row and 30 columns.
    Uses string parsing for URL structure, and heuristic defaults for network-heavy features.
    Typically, 1 = Legitimate, 0 = Suspicious, -1 = Phishing.
    """
    
    # Ensure URL has scheme for parsing
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
        
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    # 1. having_IP_Address
    having_IP_Address = 1
    try:
        ipaddress.ip_address(domain)
        having_IP_Address = -1
    except:
        pass

    # 2. URL_Length
    url_len = len(url)
    if url_len < 54:
        URL_Length = 1
    elif 54 <= url_len <= 75:
        URL_Length = 0
    else:
        URL_Length = -1

    # 3. Shortining_Service
    shorteners = ['bit.ly', 'goo.gl', 'shorte.st', 'go2l.ink', 'x.co', 'ow.ly', 't.co', 'tinyurl']
    Shortining_Service = -1 if any(short in domain for short in shorteners) else 1

    # 4. having_At_Symbol
    having_At_Symbol = -1 if '@' in url else 1

    # 5. double_slash_redirecting
    # Check if '//' appears anywhere after the initial 'http://'
    double_slash_redirecting = -1 if url.rfind('//') > 7 else 1

    # 6. Prefix_Suffix
    Prefix_Suffix = -1 if '-' in domain else 1

    # 7. having_Sub_Domain
    # Count dots in the domain (excluding www.)
    domain_clean = domain.replace('www.', '')
    dot_count = domain_clean.count('.')
    if dot_count == 1:
        having_Sub_Domain = 1
    elif dot_count == 2:
        having_Sub_Domain = 0
    else:
        having_Sub_Domain = -1

    # 8. SSLfinal_State (Defaulting to 1 as legitimate placeholder)
    SSLfinal_State = 1 if url.startswith('https') else -1

    # 9. Domain_registeration_length (Default)
    Domain_registeration_length = 1

    # 10. Favicon (Default)
    Favicon = 1

    # 11. port
    port = -1 if ':' in domain else 1

    # 12. HTTPS_token
    HTTPS_token = -1 if 'https' in domain_clean else 1

    # 13 - 30. Remaining features - Defaulting to Legitimate (1) or neutral
    features = {
        'having_IP_Address': having_IP_Address,
        'URL_Length': URL_Length,
        'Shortining_Service': Shortining_Service,
        'having_At_Symbol': having_At_Symbol,
        'double_slash_redirecting': double_slash_redirecting,
        'Prefix_Suffix': Prefix_Suffix,
        'having_Sub_Domain': having_Sub_Domain,
        'SSLfinal_State': SSLfinal_State,
        'Domain_registeration_length': Domain_registeration_length,
        'Favicon': Favicon,
        'port': port,
        'HTTPS_token': HTTPS_token,
        'Request_URL': 1,
        'URL_of_Anchor': 0, # Neutral
        'Links_in_tags': 0,
        'SFH': 1,
        'Submitting_to_email': 1,
        'Abnormal_URL': 1,
        'Redirect': 0,
        'on_mouseover': 1,
        'RightClick': 1,
        'popUpWidnow': 1,
        'Iframe': 1,
        'age_of_domain': 1,
        'DNSRecord': 1,
        'web_traffic': 1,
        'Page_Rank': -1, # Often phishing sites have low page rank
        'Google_Index': 1,
        'Links_pointing_to_page': 0,
        'Statistical_report': 1
    }

    # Ensure the exact order of columns matching the schema
    columns = [
        "having_IP_Address", "URL_Length", "Shortining_Service", "having_At_Symbol", 
        "double_slash_redirecting", "Prefix_Suffix", "having_Sub_Domain", "SSLfinal_State", 
        "Domain_registeration_length", "Favicon", "port", "HTTPS_token", "Request_URL", 
        "URL_of_Anchor", "Links_in_tags", "SFH", "Submitting_to_email", "Abnormal_URL", 
        "Redirect", "on_mouseover", "RightClick", "popUpWidnow", "Iframe", "age_of_domain", 
        "DNSRecord", "web_traffic", "Page_Rank", "Google_Index", "Links_pointing_to_page", 
        "Statistical_report"
    ]

    # Convert to DataFrame
    df = pd.DataFrame([features], columns=columns)
    return df
