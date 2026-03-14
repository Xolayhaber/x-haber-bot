import feedparser

def get_news():
    news_list = []

    with open("sources.txt", "r") as f:
        sources = f.readlines()

    for src in sources:
        feed = feedparser.parse(src.strip())

        for entry in feed.entries[:3]:
            news = {
                "title": entry.title,
                "link": entry.link
            }
            news_list.append(news)

    return news_list
