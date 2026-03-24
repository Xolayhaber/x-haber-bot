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
    ozet = ozetle(n.get("summary", ""))

    tweet = f"""📰 SON DAKİKA

{n["title"]}

🧠 Özet:
{ozet}

Kaynak: {n["link"]}
"""

    print("------ TWEET ------")
    print(tweet)
