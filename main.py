from news_fetcher import get_news

print("BOT BASLADI")

news = get_news()

for n in news[:5]:
    print("HABER:")
    print(n["title"])
    print(n["link"])
    print("------")
