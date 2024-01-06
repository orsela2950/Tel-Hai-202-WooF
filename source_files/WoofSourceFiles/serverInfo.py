import json
import filelock
import os

"""
commit for now - will be deleted
# the original server url
MAIN_URL = "http://testwaf202.com"

URL_TO_IP = {
    "http://testwaf202.com": ("127.0.0.1", 80)
}

# the servers ip and operation port
IP = "127.0.0.1"
PORT = 8000

# dont touch-
URL_IP = 'http://' + IP

MANAGER_PANEL_HOST = 'wafmanagerpanel202.com'
"""


def get_json_argument(key: str):
    with filelock.FileLock("server_properties.json.lock"):
        with findFile_Read("server_properties.json","source_files\\WoofSourceFiles") as f:
            return json.load(f)[key]

def findFile_Read(name, path):
    filePath=""
    for root, dirs, files in os.walk(os.getcwd()):
        if name in files:
            return open(os.path.join(root, name),"r")
    return open(path+"\\"+name,"a")        


def get_server_host():
    return get_json_argument('server_host')


def get_server_ip():
    return get_json_argument('server_ips_ports')[0][0]


def get_server_port():
    return get_json_argument('server_ips_ports')[0][1]


def get_server_ipead_url():
    return 'http://' + get_server_ip()


def remove_scheme(url: str):
    """removes the http/https opening from urls

    Args:
        url (str): url to strip

    Returns:
        (str): stripped url
    """
    if url.endswith('/'):
        url = url[:-1]
    if url.lower().startswith("http://"):
        return url[7:]
    if url.lower().startswith("https://"):
        return url[8:]
    return url

if __name__ == '__main__':
    # tests
    print('host: ' + str(get_server_host()))
    print('ip: ' + str(get_server_ip()))
    print('port: ' + str(get_server_port()))
