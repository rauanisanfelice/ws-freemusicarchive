from utils import ListFiles
from datetime import datetime
from json import load, dump


PATH = "./json/" 



def main():

    start_time = datetime.now()
    
    if not get_info_license_per_genres():
        return

    print(f"GET INFO LICENSES - Time: {str(datetime.now()  - start_time)}")
    

def get_info_license_per_genres() -> bool:
    
    try:
    
        get_all_licenses = lambda x: x["License"]

        files = ListFiles(PATH)
        for fileJSON in files:
            if fileJSON.find("GENRES") == -1 and fileJSON.find("INFO_LICENSES") == -1:
                with open(f'{PATH}{fileJSON}') as json_file:
                    data = load(json_file)
                    all_licenses = list(map(get_all_licenses, data))
                    unique_licenses = list(set(all_licenses))
                    result = dict(zip(list(all_licenses),[list(all_licenses).count(i) for i in list(all_licenses)]))

        with open(f'{PATH}{datetime.now().strftime("%Y%m%d")}_INFO_LICENSES.json', "w", encoding="utf-8") as fileJSON:
            dump(result, fileJSON, indent=4, ensure_ascii=False)

        return True

    except Exception as error:
        print(f"Erro ao buscar Generos - Error: {error}")
        return False


if __name__ == '__main__':

    main()
  