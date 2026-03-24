from news_fetcher import get_news

print("BOT BASLADI")

# yasaklı kelimeleri oku
with open("banned_words.txt", "r") as f:
    banned_words = [line.strip().lower() for line in f.readlines()]

def temiz_mi(metin):
    for kelime in banned_words:
        if kelime in metin.lower():
            return False
    return True

news = get_news()

for n in news[:5]:

    if not temiz_mi(n["title"]):
        print("❌ Filtreye takıldı:", n["title"])
        continue

    tweet = f"""📰 SON DAKİKA

{n["title"]}

Kaynak: {n["link"]}
"""

    print("------ TWEET ------")
    print(tweet)
