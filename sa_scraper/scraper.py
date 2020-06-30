from datetime import datetime
from typing import Dict, List
import requests
import json
import ciso8601


class SeekingAlpha:
    """"
    SeekingAlpha is the main scraper object

    Attributes
    ----------
    proxies : dict
        the requests proxy dictionary

    Methods
    -------
    fetch_news(ticker, to_date, sa_news=False)
        Fetches a batch of 100 articles

    update_proxies(new_proxies)
        Set new proxy dictionary
    """

    API_URL = "https://seekingalpha.com/api/v3/"
    NEWS_URL = API_URL + "symbols/{0}/{1}?id={0}"

    def __init__(self, proxies: Dict[str, str]) -> None:
        """
        Parameters
        ----------
        proxies : dict
            The requests proxy dict
        """
        self.s = requests.Session()
        self.s.proxies = proxies

    def update_proxies(self, new_proxies: Dict[str, str]) -> None:
        """
        Parameters
        ----------
        proxies : dict
            The requests proxy dict
        """
        self.s.proxies = new_proxies

    @staticmethod
    def __parse_news(articles, ticker: str) -> List[Dict[str, str]]:
        """
        Formats results for InfluxDB

        Parameters
        ----------
        articles : list
            The JSON result data
        ticker : str
            The ticker symbol
        """

        for x, article in enumerate(articles):
            published_at = article['attributes']['publishOn']
            title = article['attributes']['title']
            link = article['links']['self']
            # InfluxDB scheme
            articles[x]: Dict[str, str] = {
                "measurement": "news_article",
                "tags": {
                    "ticker": ticker,
                },
                "time": ciso8601.parse_datetime(published_at).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "fields": {
                    "title": title,
                    "url": link,
                },
            }
        return articles

    def fetch_news(self, ticker: str, end_date: datetime, sa_news=False):
        news_type = 'partner-news' if not sa_news else 'news'
        url = self.NEWS_URL.format(ticker.lower(), news_type)\
            + f"?filter[until]={int(end_date.timestamp())}"\
            + f"&include=author,primaryTickers,secondaryTickers,sentiments"\
              + f"&isMounting=false&page[size]=100"

        r = self.s.get(url)

        data = json.loads(r.content.decode('utf-8'))['data']

        return self.__parse_news(data, ticker)
