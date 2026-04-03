from news_fetcher import get_news
import subprocess
import requests
from datetime import datetime
import urllib.parse

print("BOT BASLADI")

BOT_TOKEN = "8598345753:AAHOU_uLZogP2ymB8FELvBs5LKWF_w-DagQ"
CHAT_ID = "82475703"

# saat kontrolü
saat = datetime.now().hour
gece_modu = (saat >= 22 or saat < 6)

# kritik kelimeler (gece için)
kritik_kelimeler = [
    "deprem",
    "saldırı",
    "savas",
    "savaş",
    "patlama",
    "ölü",
    "yaralı",
    "acil",
    "son dakika"
]

# yasaklı kelimeler
with open("banned_words.txt", "r") as f:
    banned_words = [line.strip().lower() for line in f.readlines()]

def temiz_mi(metin):
    for kelime in banned_words:
        if kelime in metin.lower():
            return False
    return True

def kritik_mi(metin):
    for kelime in kritik_kelimeler:
        if kelime in metin.lower():
            return True
    return False

# nokta kontrolü
def nokta_ekle(metin):
    metin = metin.strip()
    if not metin.endswith((".", "!", "?")):
        metin += "."
    return metin

# özetleme
def ozetle(metin):
    kelimeler = metin.split()
    if len(kelimeler) > 12:
        return " ".join(kelimeler[:12]) + "..."
    return metin

# telegram gönder
def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mesaj,
        "disable_web_page_preview": False
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

    # GECE KONTROLÜ
    if gece_modu and not kritik_mi(n["title"]):
        continue

    baslik = nokta_ekle(n["title"])

    metin = n.get("summary") if n.get("summary") else n["title"]
    ozet = ozetle(metin)

    if ozet.lower() == n["title"].lower():
        ozet = ""

    if ozet:
        ozet = nokta_ekle(ozet)

    # tweet metni
    if ozet:
        tweet_text = f"""📰 {baslik}

{ozet}

KAYNAK: {n["link"]}"""
    else:
        tweet_text = f"""📰 {baslik}

KAYNAK: {n["link"]}"""

    tweet_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet_text)

    # telegram mesajı
    mesaj = f"""{tweet_text}

📲 PAYLAŞ:
{tweet_url}
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
