import feedparser

print("Xolayhaber bot başlatıldı...")

# Teknoloji RSS kaynağı (BBC)
rss_url = "https://feeds.bbci.co.uk/news/technology/rss.xml"

feed = feedparser.parse(rss_url)

if not feed.entries:
    print("Haber bulunamadı.")
else:
    print("Çekilen ilk 5 haber:")
    for entry in feed.entries[:5]:
        print("- " + entry.title)

print("Bot işlemi tamamlandı.")
