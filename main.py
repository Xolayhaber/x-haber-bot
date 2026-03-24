from news_fetcher import get_news

print("BOT BASLADI")

def ozetle(metin):
    # basit özet (ilk 12 kelime)
    kelimeler = metin.split()
    return " ".join(kelimeler[:12]) + "..."

news = get_news()

for n in news[:5]:
    ozet = ozetle(n["title"])

    tweet = f"""📰 SON DAKİKA

{n["title"]}

🧠 Özet:
{ozet}

Kaynak: {n["link"]}
"""

    print("------ TWEET ------")
    print(tweet)
