from news_fetcher import get_news

print("BOT BASLADI")

def ozetle(metin):
    kelimeler = metin.split()

    if len(kelimeler) > 12:
        return " ".join(kelimeler[:12]) + "..."
    else:
        return metin

news = get_news()

for n in news[:5]:

    # summary yoksa title kullan
    metin = n.get("summary") if n.get("summary") else n["title"]

    ozet = ozetle(metin)

    tweet = f"""📰 SON DAKİKA

{n["title"]}

🧠 Özet:
{ozet}

Kaynak: {n["link"]}
"""

    print("------ TWEET ------")
    print(tweet)
