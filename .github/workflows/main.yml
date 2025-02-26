name: RSS to Blogger Auto Post

on:
  schedule:
    - cron: '0 * * * *' # ہر گھنٹے پر چلے گا
  workflow_dispatch: # Manual run کے لیے

jobs:
  post-to-blogger:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: pip install requests feedparser

      - name: Run script to post to Blogger
        env:
          BLOGGER_BLOG_ID: ${{ secrets.BLOGGER_BLOG_ID }}
          BLOGGER_API_KEY: ${{ secrets.BLOGGER_API_KEY }}
          RSS_FEED_URL: ${{ secrets.RSS_FEED_URL }}
        run: python script.py
