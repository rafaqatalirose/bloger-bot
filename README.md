import requests
import feedparser

# Blogger API details
BLOG_ID = '3540900078974238078'
API_KEY = 'AIzaSyDYltDDbD1pEgKAvf1k1mCtOOP7Y6ECXis'

# RSS feed URL
RSS_FEED_URL = 'https://your-rss-feed-url.com/feed'

# Function to create a blog post
def create_blog_post(title, content):
    url = f'https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts?key={API_KEY}'
    
    post_data = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    
    response = requests.post(url, json=post_data)
    if response.status_code == 200:
        print(f'Post created: {title}')
    else:
        print(f'Failed to create post: {response.status_code} - {response.text}')

# Function to fetch and post RSS feed
def fetch_and_post_rss():
    feed = feedparser.parse(RSS_FEED_URL)
    
    for entry in feed.entries[:5]:  # Post the latest 5 entries
        title = entry.title
        content = entry.summary + f'<br/><a href="{entry.link}">Read more</a>'
        create_blog_post(title, content)

if __name__ == '__main__':
    fetch_and_post_rss()


