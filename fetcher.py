import feedparser
import json
import ssl
import urllib.request
import certifi

RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml"
]
RAW_FILE = "raw.json"   # dữ liệu thô (bước trung gian — cron job sẽ tóm tắt sang data.json)

# User-Agent trình duyệt để tránh bị chặn (Python-urllib bị từ chối)
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

# Python /usr/local/bin thiếu CA cert hệ thống -> dùng certifi để verify SSL
SSL_CTX = ssl.create_default_context(cafile=certifi.where())
HTTPS_HANDLER = urllib.request.HTTPSHandler(context=SSL_CTX)


def fetch_news():
    all_entries = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url, agent=USER_AGENT, handlers=[HTTPS_HANDLER])
        if feed.bozo:
            print(f"[WARN] {url} bị chặn/không parse được")
        for entry in feed.entries[:3]:
            # Lấy cả published nếu có
            published = getattr(entry, 'published', '')
            all_entries.append({
                "source": "TechCrunch" if "techcrunch" in url else "The Verge",
                "title": entry.title,
                "link": entry.link,
                "summary": getattr(entry, 'summary', entry.title),
                "published": published,
            })
    return all_entries


if __name__ == "__main__":
    news = fetch_news()
    with open(RAW_FILE, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=4)
    print(f"Đã lưu {len(news)} tin thô vào {RAW_FILE}.")
