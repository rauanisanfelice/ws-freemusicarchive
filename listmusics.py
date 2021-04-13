import requests

from bs4 import BeautifulSoup
from math import ceil
from json import dump, load
from datetime import datetime
from os import walk
from threading import Thread
from time import sleep


TIMEOUT = 5
PATH = "./json/" 


def main():

    start_time = datetime.now()
    
    GENRE="Jazz"
    ws_list_all_tracks_per_genre(GENRE=GENRE)
    print(f"GENRE: {GENRE.upper()} - Time: {str(datetime.now()  - start_time)}")

    # GENRE="Blues"
    # ws_list_all_tracks_per_genre(GENRE=GENRE)
    # print(f"GENRE: {GENRE.upper()} - Time: {str(datetime.now()  - start_time)}")
    
    # GENRE="Folk"
    # ws_list_all_tracks_per_genre(GENRE=GENRE)
    # print(f"GENRE: {GENRE.upper()} - Time: {str(datetime.now()  - start_time)}")

    # GENRE="Electronic"
    # ws_list_all_tracks_per_genre(GENRE=GENRE)
    # print(f"GENRE: {GENRE.upper()} - Time: {str(datetime.now()  - start_time)}")
    
    # GENRE="House"
    # ws_list_all_tracks_per_genre(GENRE=GENRE)
    # print(f"GENRE: {GENRE.upper()} - Time: {str(datetime.now()  - start_time)}")

    # BUSCA TODOS OS GENEROS
    if not get_all_genres():
        return
    print(f"GET ALL GENRE: {GENRE.upper()} - Time: {str(datetime.now()  - start_time)}")

    # ANALISA LICENSA
    if not get_licenses():
        return
    print(f"GET ALL LICENSES: {GENRE.upper()} - Time: {str(datetime.now()  - start_time)}")
    

def check_health(url:str) -> bool:
    
    status_code_health = requests.get(url, timeout=TIMEOUT).status_code
    if status_code_health != 200:
        print("Erro pagina nao existe: ", url)
        print(status_code_health)
        return False
    return True


def ws_list_all_tracks_per_genre(GENRE:str) -> list:

    TOTAL_TRACKS_IN_PAGE = 0
    PAGE_SIZE = 100
    PAGE_BEGIN = 1
    SORT = "interest" # "date" or "interest"
    URL = f"https://freemusicarchive.org/genre/{GENRE}?sort={SORT}&d=0&pageSize={PAGE_SIZE}&page={PAGE_BEGIN}"

    # CHECK HEALTH PAGE
    if not check_health(URL):
        return False

    # BUSCA TOTAL DE MUSICAS
    html = requests.get(URL, timeout=5).content
    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

    info = soup.find("div", "pagination-full").find("span", "lf").find_all("b")
    TOTAL_TRACKS_IN_PAGE = int(info[len(info) - 1].string)
    PAGES = ceil(TOTAL_TRACKS_IN_PAGE / PAGE_SIZE) + 1
    print(f"GENRE: {GENRE.upper()} - TOTAL PAGES: {PAGES - 1}")

    # LOOP PAGES
    all_tracks = []
    for page_index in range(1, PAGES):
        
        start_time = datetime.now()
        URL = f"https://freemusicarchive.org/genre/{GENRE}?sort={SORT}&d=0&pageSize={PAGE_SIZE}&page={page_index}"
        if not check_health(URL):
            continue
        
        # WEB SCRAPING
        tracks = ws_info_track(URL)
        if tracks is None:
            return False
        
        all_tracks.extend(tracks)

        print(f"GENRE: {GENRE.upper()} - PAGE: {page_index} - Time: {str(datetime.now()  - start_time)}")

    with open(f'{PATH}{datetime.now().strftime("%Y%m%d")}_{GENRE.upper()}.json', "w", encoding="utf-8") as fileJSON:
        dump(all_tracks, fileJSON, indent=4, ensure_ascii=False)


def ws_info_track(url:str) -> list:
    
    try:
        
        tracks = []
        html = requests.get(url, timeout=10).content
        soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
        playlist = soup.find("div", class_="playlist")

        # VARRE LISTA DE MUSICAS
        itens = playlist.find_all("div", class_="play-item")
        for item in itens:
            
            # ARTIST
            if item.find("span", class_="ptxt-artist").a is not None:
                artist = item.find("span", class_="ptxt-artist").a.string.replace("\n", "")
                artist_url = item.find("span", class_="ptxt-artist").a.get("href")
            else:
                artist = "Not Found"
                artist_url = "Not Found"

            # TRACK
            if item.find("span", class_="ptxt-track").a is not None:
                track = item.find("span", class_="ptxt-track").a.string.replace("\n", "")
                track_url = item.find("span", class_="ptxt-track").a.get("href")
            else:
                track = "Not Found"
                track_url = "Not Found"

            # ALBUM
            if item.find("span", class_="ptxt-album").a is not None:
                album = item.find("span", class_="ptxt-album").a.string.replace("\n", "")
                album_url = item.find("span", class_="ptxt-album").a.get("href")
            else:
                album = "Not Found"
                album_url = "Not Found"

            # GENRES
            genres_list_track = []
            genres = item.find("span", class_="ptxt-genre").find_all("a")
            for genreList in genres:
                genre = genreList.string.replace("\n", "")
                genre_url = genreList.get("href")
                genres_list_track.append({
                    "Genre": genre,
                    "Genre_url": genre_url,
                })
            
            tracks.append({
                "Artist": artist,
                "Artist_url": artist_url,
                "Track": track,
                "Track_url": track_url,
                "Album": album,
                "Album_url": album_url,
                "Genres": genres_list_track,
                "License": None,
            })
    
        return tracks
        
    except Exception as error:
        print(f"Erro ao realizar WS - Erro: {error}")
        return None


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


def get_all_genres() -> bool:
    
    try:
    
        get_all_genres = lambda x: x["Genres"]
        all_genres = []

        files = ListFiles(PATH)
        for fileJSON in files:
            if fileJSON.find("GENRES") == -1:
                with open(f'{PATH}{fileJSON}') as json_file:
                    data = load(json_file)
                    all_genres_list = list(map(get_all_genres, data))
                    for list_item in all_genres_list:
                        for item in list_item:
                            all_genres.append(item["Genre"])

        with open(f'{PATH}{datetime.now().strftime("%Y%m%d")}_GENRES.json', "w", encoding="utf-8") as fileJSON:
            dump(sorted(list(set(all_genres))), fileJSON, indent=4, ensure_ascii=False)

        return True

    except Exception as error:
        print(f"Erro ao buscar Generos - Error: {error}")
        return False


def get_licenses() -> bool:
    
    try:
    
        get_all_trak_url = lambda x: { "Track_url": x["Track_url"], "index": data.index(x)}
        all_genres = []

        files = ListFiles(PATH)
        for fileJSON in files:
            if fileJSON.find("GENRES") == -1:
                with open(f'{PATH}{fileJSON}', "r") as json_file:
                    data = load(json_file)
                    list_all_track_url = list(map(get_all_trak_url, data))

                for link in list_all_track_url:
                    
                    print(f'Buscando licença: {link["index"] + 1}/{len(list_all_track_url)}') 

                    # CHECK HEALTH PAGE
                    if not check_health(link["Track_url"]):
                        data[link["index"]]["License"] = None
                        with open(f'{PATH}{fileJSON}', "w", encoding="utf-8") as json_file:
                            dump(data, json_file, indent=4, ensure_ascii=False)
                        continue
                    
                    # BUSCA LICENSE
                    html = requests.get(link["Track_url"], timeout=5).content
                    soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

                    if soup.find("div", "box-stnd-nobord") is None:
                        data[link["index"]]["License"] = None
                    elif soup.find("div", "box-stnd-nobord").find("div", "sbar-stat-multi") is None:
                        data[link["index"]]["License"] = None
                    elif soup.find("div", "box-stnd-nobord").find("div", "sbar-stat-multi").find_all("a") is None:
                        data[link["index"]]["License"] = None
                    else:
                        links_info = soup.find("div", "box-stnd-nobord").find("div", "sbar-stat-multi").find_all("a")
                        license_info = None
                        for info in links_info:
                            if info.string is not None and info.get("rel") is not None:
                                if info.get("rel")[0] == "license":
                                    license_info = info.string
                        data[link["index"]]["License"] = license_info
                    
                    with open(f'{PATH}{fileJSON}', "w", encoding="utf-8") as json_file:
                        dump(data, json_file, indent=4, ensure_ascii=False)

        return True
    
    except Exception as error:
        print(f"Erro ao buscar licença - Error: {error}")
        return False


if __name__ == '__main__':

    main()
    
    