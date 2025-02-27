import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from google.oauth2 import service_account
from google.auth.transport.requests import Request

BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
RSS_FEED_URLS = os.environ.get("RSS_FEED_URLS")  # Comma-separated URLs
SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_FILE")

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
scoped_credentials = credentials.with_scopes(['https://www.googleapis.com/auth/blogger'])

def fetch_rss(feed_url):
    try:
        response = requests.get(feed_url)
        response.raise_for_status()
        print(f"Fetched RSS feed successfully: {feed_url}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {feed_url}\n{e}")
        return None

def extract_content(rss_xml):
    soup = BeautifulSoup(rss_xml, "xml")
    items = soup.find_all("item")
    posts = []

    if not items:
        print("No items found in the RSS feed!")
    
    for item in items:
        title = item.title.text if item.title else "Untitled Post"
        link = item.link.text if item.link else ""
        description = item.description.text if item.description else "No description available."
        pub_date = item.pubDate.text if item.pubDate else datetime.now().isoformat()

        content = f"<p>{description}</p>"
        media = item.find("media:content") or item.find("enclosure")
        if media and media.get("url"):
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
    
    print(f"Extracted {len(posts)} posts from RSS feed.")
    return posts

def extract_tags(title):
    keywords = title.lower().split()
    unique_tags = list(set(keywords))
    return unique_tags[:5]

def post_to_blogger(post):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts"
    data = {
        "kind": "blogger#post",
        "title": post["title"],
        "content": post["content"],
        "labels": post["tags"]
    }
    try:
        headers = {
            'Authorization': 'Bearer ' + scoped_credentials.token
        }
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Successfully posted to Blogger: {post['title']}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Blogger: {post['title']}\n{e}")
        return None

def main():
    feed_urls = RSS_FEED_URLS.split(",")
    for feed_url in feed_urls:
        rss_xml = fetch_rss(feed_url)
        if rss_xml:
            posts = extract_content(rss_xml)
            for post in posts:
                post_to_blogger(post)

if __name__ == "__main__":
    main()
