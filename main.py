from news_fetcher import get_news
import subprocess

print("BOT BASLADI")

# yasaklı kelimeler
with open("banned_words.txt", "r") as f:
    banned_words = [line.strip().lower() for line in f.readlines()]

def temiz_mi(metin):
    for kelime in banned_words:
        if kelime in metin.lower():
            return False
    return True

# kalite filtresi
def kaliteli_mi(metin):
    anahtarlar = [
        "son dakika",
        "açıkladı",
        "karar",
        "duyurdu",
        "yasak",
        "onay",
        "gelişme",
        "zam",
        "deprem",
        "indirim"
    ]

    for kelime in anahtarlar:
        if kelime in metin.lower():
            return True
    return False

# daha önce paylaşılanlar
try:
    with open("posted_links.txt", "r") as f:
        posted = set(line.strip() for line in f.readlines())
except:
    posted = set()

news = get_news()
yeni_linkler = []

for n in news:

    if n["link"] in posted:
        continue

    if not temiz_mi(n["title"]):
        continue

    if not kaliteli_mi(n["title"]):
        continue

    tweet = f"""📰 SON DAKİKA

{n["title"]}

Kaynak: {n["link"]}
"""

    print("------ TWEET ------")
    print(tweet)

    yeni_linkler.append(n["link"])

# yeni linkleri kaydet
with open("posted_links.txt", "a") as f:
    for link in yeni_linkler:
        f.write(link + "\n")

# github'a kaydet
subprocess.run(["git", "config", "--global", "user.email", "bot@github.com"])
subprocess.run(["git", "config", "--global", "user.name", "bot"])
subprocess.run(["git", "add", "posted_links.txt"])
subprocess.run(["git", "commit", "-m", "update links"])
subprocess.run(["git", "push"])
