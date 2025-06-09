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
print(followed_manga[1])
wb = openpyxl.load_workbook("Manga and Good Omens.xlsx")
ws = wb.active

for manga in followed_manga: 
    title = manga["data"]["attributes"]["title"]["en"]
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
        artist_list += data["data"]["attributes"]["name"] + ", "


    ws.append()
