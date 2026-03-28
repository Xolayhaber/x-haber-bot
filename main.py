from news_fetcher import get_news
import subprocess
import urllib.parse

print("BOT BASLADI")

# yasaklı kelimeler
with open("banned_words.txt", "r") as f:
    banned_words = [line.strip().lower() for line in f.readlines()]

def temiz_mi(metin):
    for kelime in banned_words:
        if kelime in metin.lower():
            return False
    return True

# özetleme
def ozetle(metin):
    kelimeler = metin.split()
    if len(kelimeler) > 10:
        return " ".join(kelimeler[:10]) + "..."
    return metin

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
        print("❌ Filtre:", n["title"])
        continue

    # özet için summary varsa kullan
    metin = n.get("summary") if n.get("summary") else n["title"]
    ozet = ozetle(metin)

    # eğer özet başlıkla aynıysa kaldır
    if ozet.lower() == n["title"].lower():
        ozet = ""

    # tweet oluştur
    if ozet:
        tweet_text = f"""📰 {n["title"]}

{ozet}

🔗 Kaynak: {n["link"]}
"""
    else:
        tweet_text = f"""📰 {n["title"]}

🔗 Kaynak: {n["link"]}
"""

    tweet_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet_text)

    print("------ PAYLAŞ ------")
    print(tweet_text)
    print("👉", tweet_url)

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
