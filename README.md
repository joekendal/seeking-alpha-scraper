### Description
Tool for grabbing news articles from SeekingAlpha's backend API. Useful for populating a time-series database. Requires proxies to bypass rate limits.

### Usage
```python
from sa_scraper import SeekingAlpha

sa = SeekingAlpha(
    proxies=dict(
        http='socks5://localhost:9050',
        https='socks5://localhost:9050',
    )
)

symbol = "TSLA"
end_date = datetime.utcnow()

articles = sa.fetch_news(symbol, end_date)

print(json.dumps(articles, indent=4))
```