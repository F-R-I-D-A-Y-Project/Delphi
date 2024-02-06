import os
import requests
import argparse
import pathlib
import json
from dotenv import load_dotenv


base_url = 'https://www.alphavantage.co/query?'

load_dotenv()


def get_user_input():
    parser = argparse.ArgumentParser(
        description='Get historical data from a company')
    parser.add_argument('-s', '--symbol', type=str,
                        help='Company symbol', required=True)
    parser.add_argument('-r', '--resolution', type=str,
                        help='Resolution of the data', required=True)
    parser.add_argument('-i', '--interval', type=str,
                        help='Interval of the data')
    parser.add_argument('-z', '--size', type=str, help='Size of the data', default='full')

    args = parser.parse_args()
    return args


def check_inputs(function: str, symbol: str, interval: str, outputsize: str) -> None:
    if function == 'intraday' and interval not in ['1min', '5min', '15min', '30min', '60min']:    
        raise ValueError('Invalid interval: Inexistent or not supported. Please use 1min, 5min, 15min, 30min or 60min.')
    if function != 'intraday' and interval:
        raise ValueError('Invalid interval: Intraday data does not support interval.')
    if outputsize not in ['compact', 'full']:
        raise ValueError('Invalid outputsize: Inexistent or not supported. Please use compact or full.')
    if len(symbol) > 5:
        raise ValueError('Invalid symbol: Symbol length must be less than 5 characters.')

def get_url(user_input: argparse.Namespace) -> str:
    symbol = user_input.symbol.upper()
    function: str
    apikey = os.getenv('API_KEY')
    interval = user_input.interval
    outputsize = user_input.size

    check_inputs(user_input.resolution, symbol, interval, outputsize)
    if user_input.resolution == 'intraday':
        function = 'TIME_SERIES_INTRADAY'
    elif user_input.resolution == 'daily':
        function = 'TIME_SERIES_DAILY'
    elif user_input.resolution == 'weekly':
        function = 'TIME_SERIES_WEEKLY'
    else:
        raise ValueError(
            'Invalid function: Inexistent or not supported. Please use intraday, daily or weekly.')

    if function != 'TIME_SERIES_INTRADAY':
        print(f'{base_url}function={function}&symbol={symbol}&apikey={apikey}&outputsize={outputsize}')
        return f'{base_url}function={function}&symbol={symbol}&apikey={apikey}&outputsize={outputsize}', symbol
    return f'{base_url}function={function}&symbol={symbol}&interval={interval}&apikey={apikey}&outputsize={outputsize}', symbol

def get_download_folder():
    return pathlib.Path(os.path.expanduser('~')) / 'Downloads'

def scrape_data(url: str) -> None:
    r = requests.get(url)
    return r.json()


def store_data(data: dict, company: str) -> None:
    if not pathlib.Path('data').exists():
        pathlib.Path('data').mkdir()
    with open(f'data/{company}.json', 'w') as f:
        json.dump(data, f)


def main():
    url, company = get_url(get_user_input())
    data = scrape_data(url)
    store_data(data, company)


if __name__ == '__main__':
    main()
