from datetime import datetime, timedelta, date

from slack import WebClient
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
        self._settings = _settings

    @property
    def status(self):
        return self._settings['status']

    @property
    def token(self):
        return self._settings['token']

    @property
    def channels(self):
        return self._settings['channels']

    @property
    def tags(self):
        return self._settings['tags']

    @property
    def freq(self):
        return self._settings['freq']

    @property
    def start_date(self):
        return self._settings['start_date']

    @property
    def start_time(self):
        return self._settings['start_time']

    @property
    def max_article(self):
        return self._settings['max_article']

    @property
    def last_article_time(self):
        return self._settings['last_article_time']

    @property
    def last_article_id(self):
        return self._settings['last_article_id']

    @property
    def text(self):
        return self._settings['text']


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
    def __init__(self, url, sheet):
        self.url = url
        self.sheet = sheet
        self.header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        self.response = None

    def __str__(self):
        return self.response

    def get_page(self):
        try:
            response = requests.get(self.url+self.sheet, headers=self.header, timeout=5)
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
        soup = BeautifulSoup(self.page, 'lxml')
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


class Slack:
    def __init__(self):
        self.settings = Settings()
        self.token = self.settings.token
        self.all_channels = self.get_channels()
        self.channels = self.settings.channels
        self.id_channel = self.get_id_channel(self.channels)
        self.header_message = self.settings.text
        self.freq = self.settings.freq

    def get_channels(self):
        data = {'token': self.token}
        data_slack = requests.post(url='https://slack.com/api/conversations.list', data=data).json()
        if data_slack['ok']:
            self.all_channels = {}
            for channel in data_slack['channels']:
                self.all_channels[channel['name']] = channel['id']
            return self.all_channels
        else:
            return False

    def get_id_channel(self, my_channel):
        if self.all_channels and my_channel in self.all_channels:
            return self.all_channels[my_channel]
        else:
            return False

    def write_to_channel(self):
        text = ''
        for n in range(1, 10):
            page_blog = Page('https://habr.com/ru/company/skillfactory/blog/', f'page{n}')
            if page_blog.get_page() is not None:
                parser = Parser(page_blog.response)
                articles = parser.get_articles()
                ago = date.today() - timedelta(days=self.freq)
                ago = datetime(year=ago.year, month=ago.month, day=ago.day)
                for article in articles:
                    if article.publication_time > ago:
                        text += f'• <{article.url}|{article.name}>\n'
                    else:
                        break
                else:
                    continue
                break
        if text:
            text = self.header_message + '\n' + text
            return self.request(text)
        else:
            return None

    def request(self, message):
        data = {
            'token': self.token,
            'channel': self.id_channel,    # User ID.
            'as_user': True,
            "text": message
            }
        r = requests.post(url='https://slack.com/api/chat.postMessage', data=data).json()
        return r


if __name__ == '__main__':
    program = Slack()
    program.write_to_channel()
