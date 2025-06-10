import requests
import openpyxl

login_data = {
    "username": "gaysicle",
    "password": "vurwAk-qehhub-2hawky"
}

res = requests.post("https://api.mangadex.org/auth/login", json=login_data)
tokens = res.json()["token"]
session_token = tokens["session"]
headers = {
    "Authorization": f"Bearer {session_token}"
}

# print(headers)

followed_manga = []
limit = 100
offset = 0

# while True:
url = f"https://api.mangadex.org/manga/status?status=completed"
res = requests.get(url, headers=headers)
data = res.json()
for manga in data["statuses"]:
    id = manga
    url2 = f"https://api.mangadex.org/manga/{id}"
    res2 = requests.get(url2, headers=headers)
    mangaData = res2.json()
    followed_manga.append(mangaData)

    # if len(data["data"]) < limit:
    #     break
    # offset += limit

# print(len(followed_manga))
# for manga in followed_manga:
#     print(manga)
wb = openpyxl.load_workbook("Manga and Good Omens.xlsx")
ws = wb.active

#raw and engtl
for manga in followed_manga: 
    title = manga["data"]["attributes"]["title"]["en"]
    tags = ", ".join([tag["attributes"]["name"]["en"] for tag in manga["data"]["attributes"]["tags"]])
    pub = manga["data" ]["type"]

    if "Girls' Love" in tags:
        queer = "GL"
    elif "Boys' Love" in tags:
        queer = "BL"
    else: 
        queer = "X"

    desc = manga["data"]["attributes"]["description"]["en"]

    content_rating = manga["data"]["attributes"]["contentRating"]

    source = ""
    
    if manga["data"]["attributes"]["links"]["raw"]:
        source += manga["data"]["attributes"]["links"]["raw"] + " "
    if manga["data"]["attributes"]["links"]["engtl"]:
        source += manga["data"]["attributes"]["links"]["engtl"] + " "


    artists = []
    authors = []
    for thing in manga["data"]["relationships"]:
        if thing[type] == "artist":
            artists.append(thing)
        elif thing[type] == "author":
            authors.append(thing)
        else:
            break

    artist_list = ""
    artist_links = ""
    author_list = ""
    author_links = ""

    for artist in artists:
        url = f"https://api.mangadex.org/author/{artist}"
        res = requests.get(url, headers=headers)
        data = res.json()
        artist_list = ", ".join([data["data"]["attributes"]["name"]])
        if data["data"]["attributes"]["twitter"]:
            artists_links += " " + data["data"]["attributes"]["twitter"]
        elif data["data"]["attributes"]["weibo"]:
            artists_links += " " + data["data"]["attributes"]["weibo"]
    for author in authors:
        url = f"https://api.mangadex.org/author/{author}"
        res = requests.get(url, headers=headers)
        data = res.json()
        author_list = ", ".join([data["data"]["attributes"]["name"]])
        if data["data"]["attributes"]["twitter"]:
            authors_links += " " + data["data"]["attributes"]["twitter"]
        elif data["data"]["attributes"]["weibo"]:
            authors_links += " " + data["data"]["attributes"]["weibo"]



    if artist_links: 
        ws.append([title, artist_list, author_list, artist_links, queer, content_rating, pub, tags, desc, source, "Completed", "", ""])
    elif author_links:
        ws.append([title, artist_list, author_list, author_links, queer, content_rating, pub, tags, desc, source, "Completed", "", ""])
    else:
        ws.append([title, artist_list, author_list, "n/a", queer, content_rating, pub, tags, desc, source, "Completed", "", ""])
