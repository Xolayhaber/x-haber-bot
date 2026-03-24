from news_fetcher import get_news

print("BOT BASLADI")

news = get_news()

for n in news[:5]:

    tweet = f"""📰 SON DAKİKA

{n["title"]}

Kaynak: {n["link"]}
"""

    print("------ TWEET ------")
    print(tweet)
