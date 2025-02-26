import os
import requests

BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
API_KEY = os.environ.get("BLOGGER_API_KEY")
RSS_FEED_URL = os.environ.get("RSS_FEED_URL")


def fetch_rss():
    response = requests.get(RSS_FEED_URL)
    if response.status_code == 200:
        return response.text
    else:
        return None


def post_to_blogger(title, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}"
    data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    response = requests.post(url, json=data)
    return response.json()


if __name__ == "__main__":
    rss_content = fetch_rss()
    if rss_content:
        # Example: posting static content (we can parse RSS later)
        post_to_blogger("New Post from RSS", rss_content)
        print("Post created successfully!")
    else:
        print("Failed to fetch RSS feed.")
