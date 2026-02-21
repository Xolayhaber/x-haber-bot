print("TEST BAŞLADI")

import feedparser

rss_url = "https://feeds.bbci.co.uk/news/technology/rss.xml"
feed = feedparser.parse(rss_url)

print("Toplam haber sayısı:", len(feed.entries))

for entry in feed.entries[:3]:
    print("Haber:", entry.title)

print("TEST BİTTİ")
