# the original server url
MAIN_URL = "http://testwaf202.com"

URL_TO_IP = {
    "http://testwaf202.com" : ("127.0.0.1", 80)
}

# the servers ip and operation port
IP = "127.0.0.1"
PORT = 80

# dont touch-
URL_IP = 'http://' + IP


def getIpFromUrl(urlIn : str):        
    for url in URL_TO_IP:
        if remove_HTTP_and_HTTPS(url).lower() == remove_HTTP_and_HTTPS(urlIn).lower():
            return URL_TO_IP[url]
    return None
        
        
def remove_HTTP_and_HTTPS(url : str):
    if url.lower().startswith("http://"):
        return url[7:]
    if url.lower().startswith("https://"):
        return url[8:]
    return url