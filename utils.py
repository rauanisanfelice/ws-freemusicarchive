import requests

from os import walk


TIMEOUT = 5



def ListFiles(path: str) -> list:
    """
    Function that get all files in path
    
    param:
        * path

    return:
        * listFiles(list) 
    """

    listFiles = []
    for (dirpath, dirnames, filenames) in walk(path):
        return filenames

    return None


def CheckHealth(url:str) -> bool:
    
    status_code_health = requests.get(url, timeout=TIMEOUT).status_code
    if status_code_health != 200:
        print("Erro pagina nao existe: ", url)
        print(status_code_health)
        return False
    return True

