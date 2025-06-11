import requests
import openpyxl
import os

login_data = {
    "username": "gaysicle",
    "password": os.getenv("SECRETS")
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
sheet = "Manga and Good Omens.xlsx"
wb = openpyxl.load_workbook(sheet)
ws = wb.active
n = 0
#raw and engtl
for manga in followed_manga: 
    title = manga["data"]["attributes"]["title"].get("en")
    if not title:
        title = next(iter(manga["data"]["attributes"]["title"].values()), "")

    tags = ", ".join([tag["attributes"]["name"]["en"] for tag in manga["data"]["attributes"]["tags"]])
    pub = manga["data" ]["type"]

    if "Girls' Love" in tags:
        queer = "GL"
    elif "Boys' Love" in tags:
        queer = "BL"
    else: 
        queer = "X"

    desc = manga["data"]["attributes"]["description"].get("en")
    if not desc:
        # fallback to any available language or leave it empty
        desc = next(iter(manga["data"]["attributes"]["description"].values()), "")

    content_rating = manga["data"]["attributes"]["contentRating"]

    source = ""
    
    if "raw" in manga["data"]["attributes"]["links"]:
        source += manga["data"]["attributes"]["links"]["raw"] + " "
    if "engtl" in manga["data"]["attributes"]["links"]:
        source += manga["data"]["attributes"]["links"]["engtl"] + " "


    artists = []
    authors = []
    for thing in manga["data"]["relationships"]:
        if thing["type"] == "artist":
            artists.append(thing["id"])
        elif thing["type"] == "author":
            authors.append(thing["id"])
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
            artist_links += " " + data["data"]["attributes"]["twitter"]
        elif data["data"]["attributes"]["weibo"]:
            artist_links += " " + data["data"]["attributes"]["weibo"]
    for author in authors:
        url = f"https://api.mangadex.org/author/{author}"
        res = requests.get(url, headers=headers)
        data = res.json()
        author_list = ", ".join([data["data"]["attributes"]["name"]])
        if data["data"]["attributes"]["twitter"]:
            author_links += " " + data["data"]["attributes"]["twitter"]
        elif data["data"]["attributes"]["weibo"]:
            author_links += " " + data["data"]["attributes"]["weibo"]


    n += 1

    if artist_links: 
        print(n)
        ws.append([title, artist_list, author_list, artist_links, queer, content_rating, pub, tags, desc, source, "Completed", "", ""])
    elif author_links:
        print(n)
        ws.append([title, artist_list, author_list, author_links, queer, content_rating, pub, tags, desc, source, "Completed", "", ""])
    else:
        print(n)
        ws.append([title, artist_list, author_list, "n/a", queer, content_rating, pub, tags, desc, source, "Completed", "", ""])

wb.save(sheet)