import requests
from bs4 import BeautifulSoup
# from pyspark.sql import SparkSession
import pandas as pd
def item_search(item):
    news = f"https://www.iflscience.com/{item}/latest"

    html = requests.get(news).text

    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_article(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find('div', {'id': 'Article'})
    headline = article.find("h1", {"class": "article__header__title"}).get_text()
    author = article.find("p", {"class": "author__name"}).get_text()
    published = article.find("span", {"class": "publishedDate"}).get_text()
    content = article.find("article", {"class":"main__body article-content"}).get_text()
    labels = article.find_all("a", {"class": "label"})
    categories = []
    for label in labels:
        categories.append(label.get_text())

    categories = (list(dict.fromkeys(categories)))

    return {
        "headline": headline,
        "author": author,
        "published": published,
        "content": content,
        "categories": categories,
        "link": link
    }


def page_crawler(url, label):

    links = []
    articles = []
    result = item_search(label)

    if result:
        news_div = result.find("div", {"class": "card-list"})
        all_cards = news_div.find_all("div", {"class": "card-content--body--title"})
        for card in all_cards:
            links.append(f"{url}{card.find('a')['href']}")

        for link in links:
            content = get_article(link)
            articles.append(content)

        df = pd.DataFrame(articles)
        df.to_csv(f"{label}.csv", index=False)
if __name__ == '__main__':
    label = 'humans'
    url = "https://www.iflscience.com"

    page_crawler(url, label)

