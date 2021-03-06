import argparse
import logging
import re
from requests.exceptions import HTTPError
from urllib3.exceptions import MaxRetryError

from common import config
import news_page_object as news

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
is_well_formed_link = re.compile(r'^https?://.+/.+$')  # https://example.com/hello
is_root_path = re.compile(r'^/.+$')  # /some-text


def _news_scraper(news_site_uid):
    host = config()["news_site"][news_site_uid]["url"]
    logging.info(f"Beginning scraper for {host}")
    homepage = news.HomePage(news_site_uid, host)
    
    articles = []
    for link in homepage.article_links:
        article = _fetch_article(news_site_uid, host, link)
        if article:
            logger.info("Article fetched!!")
            articles.append(article)
            print(article.title)
    print(len(articles))

def _fetch_article(news_site_uid, host, link):    
    logger.info(f"Start fetching article at {link}")
    article = None
    try:
        article = news.ArticlePage(news_site_uid, _build_link(host, link))
    except (HTTPError, MaxRetryError) as e:
        logger.warning("Error while fetching the article", exc_info=False)
    if article and not article.body:
        logger.warning("Invalid article. There is no body")
        return None
    return article
        
def _build_link(host, link):
    if is_well_formed_link.match(link):
        return link
    elif is_root_path.match(link):
        return f"{host}{link}"
    else:
        return f"{host}/{link}"
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    news_site_choices = list(config()['news_site'].keys())  # list of keys
    parser.add_argument("news_site",
                        help="The news site you want tow scrape",
                        type=str,
                        choices=news_site_choices)

    args = parser.parse_args()
    _news_scraper(args.news_site)
