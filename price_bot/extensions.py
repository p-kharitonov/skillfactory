import requests
import json
from config import TOKEN_CURRENCY, keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except KeyError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={TOKEN_CURRENCY}&symbols={quote_ticker},{base_ticker}&format=1')
        total_quote = json.loads(r.content)['rates'][keys[quote]]
        total_base = json.loads(r.content)['rates'][keys[base]]
        result = round((total_base * amount) / total_quote, 6)
        return result
