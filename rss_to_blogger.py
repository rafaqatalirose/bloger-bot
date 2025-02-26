import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
API_KEY = os.environ.get("BLOGGER_API_KEY")
RSS_FEED_URLS = os.environ.get("RSS_FEED_URLS")  # Comma-separated URLs


def fetch_rss(feed_url):
    response = requests.get(feed_url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def extract_content(rss_xml):
    soup = BeautifulSoup(rss_xml, "xml")
    items = soup.find_all("item")
    posts = []

    for item in items:
        title = item.title.text
        link = item.link.text
        description = item.description.text
        pub_date = item.pubDate.text if item.pubDate else datetime.now().isoformat()

        content = f"<p>{description}</p>"
        media = item.find("media:content") or item.find("enclosure")
        if media:
            content += f'<video controls style="max-width: 100%; height: auto;">' \
           f'<source src="{media["url"]}" type="video/mp4">' \
           'Your browser does not support the video tag.' \
           '</video>'

        
        tags = extract_tags(title)
        
        posts.append({
            "title": title,
            "content": content,
            "tags": tags,
            "link": link,
            "pub_date": pub_date
        })
    return posts


def extract_tags(title):
    keywords = title.lower().split()
    unique_tags = list(set(keywords))
    return unique_tags[:5]


def post_to_blogger(post):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}"
    data = {
        "kind": "blogger#post",
        "title": post["title"],
        "content": post["content"],
        "labels": post["tags"]
    }
    response = requests.post(url, json=data)
    return response.json()


if __name__ == "__main__":
    feed_urls = RSS_FEED_URLS.split(",")
    for feed_url in feed_urls:
        print(f"Using RSS feed URL: {feed_url.strip()}")
        rss_content = fetch_rss(feed_url.strip())
        if rss_content:
            posts = extract_content(rss_content)
            for post in posts:
                response = post_to_blogger(post)
                if response.get("id"):
                    print(f"Post '{post['title']}' created successfully!")
                else:
                    print(f"Failed to create post: {response}")
        else:
            print(f"Failed to fetch RSS feed: {feed_url}")

    print("Blog updated successfully!")
