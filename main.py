import argparse
from common import config
import logging
import news_page_object as news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _news_scraper(news_site_uid):
    host = config()["news_site"][news_site_uid]["url"]
    logging.info(f"Beinning scraper fo {host}")
    homepage = news.HomePage(news_site_uid, host)
    
    for link in homepage.article_links:
        print(link)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    news_site_choices = list(config()['news_site'].keys())  # list of keys
    parser.add_argument("news_site",
                        help="The news site you want to scrape",
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)
