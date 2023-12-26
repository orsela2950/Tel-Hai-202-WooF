# the original server url
MAIN_URL = "http://testwaf202.com"

URL_TO_IP = {
    "http://testwaf202.com" : ("127.0.0.1", 80)
}

# the servers ip and operation port
IP = "127.0.0.1"
PORT = 8000

# dont touch-
URL_IP = 'http://' + IP

MANAGER_PANEL_HOST = 'wafmanagerpanel202.com'


def getIpFromUrl(urlIn : str):        
    for url in URL_TO_IP:
        if remove_scheme(url).lower() == remove_scheme(urlIn).lower():
            return URL_TO_IP[url]
    return None
        
        
def remove_scheme(url : str):
    """removes the http/https opening from urls

    Args:
        url (str): a url to strip

    Returns:
        (str): mstripped url
    """
    if url.lower().startswith("http://"):
        return url[7:]
    if url.lower().startswith("https://"):
        return url[8:]
    return url