import pandas as pd
import os

from requests import get
from bs4 import BeautifulSoup


def get_article_text(url):
    # if we already have the data, read it locally
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.title.text
    article = soup.main.article.text.replace('\xa0', ' ')
    
    return title, article

def get_articles_from_topic(url):
    headers = {'User-Agent': 'Codeup Data Science'}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    output = []
    articles = soup.select(".news-card")
    for article in articles: 
        title = article.select("[itemprop='headline']")[0].get_text()
        body = article.select("[itemprop='articleBody']")[0].get_text()
        author = article.select(".author")[0].get_text()
        published_date = article.select(".time")[0]["content"]
        category = response.url.split("/")[-1]
        article_data = {
            'title': title,
            'body': body,
            'category': category,
            'author': author,
            'published_date': published_date,
        }
        output.append(article_data)
    return output

def get_news_articles(urls):
    output = []
    for url in urls:
        output.extend(get_articles_from_topic(url))
    df = pd.DataFrame(output)
    df.to_csv('inshorts_news_articles.csv')
    return df