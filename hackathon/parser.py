from datetime import datetime

import requests
from bs4 import BeautifulSoup
import yaml


class Settings:
    def __init__(self):
        self._settings = None
        self.load_settings()

    def load_settings(self):
        _path = 'settings.yaml'
        with open(_path, encoding='utf8') as f:
            _settings = yaml.safe_load(f)
        _settings['freq'] = _settings['freq'] - 1
        self._settings = _settings

    @property
    def settings(self):
        return self._settings


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

    def get_time(self):
        return self.publication_time


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
        _now = datetime.now()
        months = {'января': '1', 'февраля': '2', 'марта': '3', 'апреля': '4',
                  'мая': '5', 'июня': '6', 'июля': '7', 'августа': '8',
                  'сентября': '9', 'октября': '10', 'ноября': '11', 'декабря': '12',
                  'вчера': f'{_now.day - 1} {_now.month} {_now.year}', 'сегодня': f'{_now.day} {_now.month} {_now.year}'}
        for old, new in months.items():
            time = time.lower().replace(old, new)
        time = datetime.strptime(time, "%d %m %Y в %H:%M")
        return time


class Slack:
    def __init__(self, token):
        self.token = token
        self.channels = self.get_channels()

    def get_channels(self):
        data = {'token': self.token}
        data_slack = requests.post(url='https://slack.com/api/conversations.list', data=data).json()
        if data_slack['ok']:
            self.channels = {}
            for channel in data_slack['channels']:
                self.channels[channel['name']] = channel['id']
            return self.channels
        else:
            return False

    def get_id_my_channel(self, my_channel):
        if self.channels and my_channel in self.channels:
            return self.channels[my_channel]
        else:
            return False

    def write_to_channel(self, channel_id, text):
        data = {
            'token': self.token,
            'channel': channel_id,    # User ID.
            'as_user': True,
            'mrkdwn': True,
            'text': text
        }
        r = requests.post(url='https://slack.com/api/chat.postMessage', data=data).json()
        return r


if __name__ == '__main__':
    settings = Settings()
    page_blog = Page('https://habr.com/ru/company/skillfactory/blog/')
    if page_blog.get_page() is not None:
        parser = Parser(page_blog.response)
        articles = parser.get_articles()
        now = datetime.now()
        text = settings.settings['text'] + '\n'
        workspace = Slack(settings.settings['token'])
        my_id = workspace.get_id_my_channel(settings.settings['channel'])
        for article in articles:
            if article.publication_time > datetime(now.year, now.month, now.day - settings.settings['freq']):
                text += f'• <{article.url}|{article.name}>\n'
        print(workspace.write_to_channel(my_id, text))


