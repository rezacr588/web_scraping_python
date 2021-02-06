import requests
import json
from bs4 import BeautifulSoup


def save_function(article_list):
    with open('articles.json', 'w') as outfile:
        json.dump(article_list, outfile)


def hackernews_rss():
    article_list = []
    try:
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features="lxml-xml")
        articles = soup.findAll('item')
        for a in articles:
            title = a.title.string
            link = a.link.string
            published = a.pubDate.string
            article = {
                'title': title,
                'link': link,
                'published': published
            }
            article_list.append(article)
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. see exception:')
        print(e)


print('Starting Scraping')
hackernews_rss()
print('Finished Scraping')
