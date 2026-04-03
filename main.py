from news_fetcher import get_news
import subprocess
import requests

print("BOT BASLADI")

BOT_TOKEN = "8598345753:AAHOU_uLZogP2ymB8FELvBs5LKWF_w-DagQ"
CHAT_ID = "82475703"

# yasaklı kelimeler
with open("banned_words.txt", "r") as f:
    banned_words = [line.strip().lower() for line in f.readlines()]

def temiz_mi(metin):
    for kelime in banned_words:
        if kelime in metin.lower():
            return False
    return True

# nokta kontrolü
def nokta_ekle(metin):
    metin = metin.strip()
    if not metin.endswith((".", "!", "?")):
        metin += "."
    return metin

# özetleme
def ozetle(metin):
    kelimeler = metin.split()
    if len(kelimeler) > 10:
        return " ".join(kelimeler[:10]) + "..."
    return metin

# telegram gönder
def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }
    requests.post(url, data=data)

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

    baslik = nokta_ekle(n["title"])

    metin = n.get("summary") if n.get("summary") else n["title"]
    ozet = ozetle(metin)

    if ozet.lower() == n["title"].lower():
        ozet = ""

    if ozet:
        ozet = nokta_ekle(ozet)

    if ozet:
        mesaj = f"""📰 {baslik}

{ozet}

🔗 {n["link"]}
"""
    else:
        mesaj = f"""📰 {baslik}

🔗 {n["link"]}
"""

    print("GÖNDERİLDİ:", baslik)
    telegram_gonder(mesaj)

    yeni_linkler.append(n["link"])

# kaydet
with open("posted_links.txt", "a") as f:
    for link in yeni_linkler:
        f.write(link + "\n")

# github commit
subprocess.run(["git", "config", "--global", "user.email", "bot@github.com"])
subprocess.run(["git", "config", "--global", "user.name", "bot"])
subprocess.run(["git", "add", "posted_links.txt"])
subprocess.run(["git", "commit", "-m", "update links"])
subprocess.run(["git", "push"])
