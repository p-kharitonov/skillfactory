from datetime import datetime

import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, name, url, publication_time, like, tags):
        self.name = name
        self.url = url
        self.id = self.get_id(url)
        self.publication_time = publication_time
        self.like = like
        self.tags = tags

    def __str__(self):
        return f'{self.name} - {self.publication_time.strftime("%d.%m.%Y %H:%M")}'

    @staticmethod
    def get_id(url):
        _id = url.split('/')[-2]
        if _id.isdigit():
            return int(_id)
        else:
            return 0


class Page:
    def __init__(self, url):
        self.url = url
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        self.response = None

    def __str__(self):
        return self.response

    def get_page(self):
        try:
            response = requests.get(self.url, headers=self.header, timeout=5)
            if response.status_code == 200:
                self.response = response.text
                return response.text
            else:
                return None
        except requests.ConnectionError:
            print("Ошибка подключения. Убедитесь, что вы подключены к Интернету.")
            return None
        except requests.Timeout:
            print("Ошибка тайм-аута.")
            return None
        except requests.RequestException:
            print("Общая ошибка. Проверьте правильность ссылки.")
            return None
        except KeyboardInterrupt:
            print("Кто-то закрыл программу.")


class Parser:
    def __init__(self, page):
        self.page = page

    def get_articles(self):
        db = []
        soup = BeautifulSoup(self.page, 'html.parser')
        _articles = soup.select('ul > li > article.post.post_preview')
        for _article in _articles:
            name = _article.find('h2').text.strip()
            url = _article.find('h2').find('a').get('href')
            publication_time = _article.find('span', class_='post__time').text
            publication_time = self.get_time(publication_time)
            like = _article.find('span', class_='post-stats__result-counter').text
            tags = []
            hubs = _article.select('ul.post__hubs > li')
            for hub in hubs:
                tags.append(hub.find('a').text)
            db.append(Article(name, url, publication_time, like, tags))
        return db

    @staticmethod
    def get_time(time):
        now = datetime.now()
        months = {'января': '1', 'февраля': '2', 'марта': '3', 'апреля': '4',
                  'мая': '5', 'июня': '6', 'июля': '7', 'августа': '8',
                  'сентября': '9', 'октября': '10', 'ноября': '11', 'декабря': '12',
                  'вчера': f'{now.day - 1} {now.month} {now.year}', 'сегодня': f'{now.day} {now.month} {now.year}'}
        for old, new in months.items():
            time = time.lower().replace(old, new)
        time = datetime.strptime(time, "%d %m %Y в %H:%M")
        return time


if __name__ == '__main__':
    page_blog = Page('https://habr.com/ru/company/skillfactory/blog/')
    if page_blog.get_page() is not None:
        parser = Parser(page_blog.response)
        articles = parser.get_articles()
        for article in articles:
            print(article)
