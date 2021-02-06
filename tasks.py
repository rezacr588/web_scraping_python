from celery import Celery
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from celery.schedules import crontab # scheduler

app = Celery('tasks')

# schedule task execution
app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'tasks.hackernews_rss',
        'schedule': crontab()
    }
}

@app.task
def save_function(article_list):
    # timestamp and filename
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    filename = 'articles-{}.json'.format(timestamp)

    # creating our articles file with timestamp
    with open(filename, 'w') as outfile:
        json.dump(article_list, outfile)


@app.task
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
                'published': published,
                'created_at': str(datetime.now()),
                'source': 'HackerNews RSS'
            }
            article_list.append(article)
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. see exception:')
        print(e)


print('Starting Scraping')
hackernews_rss()
print('Finished Scraping')
