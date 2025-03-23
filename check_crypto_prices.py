#!/usr/bin/env python
# Crypto Prices Notification
from subprocess import run
from requests import Session
from os import path
from pygame import mixer
from dotenv import get_key
import json

# Paths
base_path = path.abspath(path.dirname(__file__))
notif_sound = path.join(base_path, 'magic-notification-ring.wav')
env_path = path.join(base_path, '.env')

# API setup
url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
api_key = get_key(env_path, 'API_KEY')

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}

session = Session()
session.headers.update(headers)

def play_sound():
    mixer.init()
    sound = mixer.Sound(notif_sound)
    sound.play()

def get_response_multiple(symbols: list):
    params = {'symbol': ','.join(symbols)}
    response = session.get(url, params=params)
    return response.json()

def get_cleaned_prices(symbols: list, symbol_names: dict):
    data = get_response_multiple(symbols)
    prices = {}
    for symbol in symbols:
        for entry in data['data'][symbol]:
            name = entry['name']
            if symbol_names[symbol] != name:
                continue
            price = entry['quote']['USD']['price']
            prices[name] = f'{price:.2f}'
    return prices

def build_message(data: dict):
    return '\n'.join(f'{k} - ${v}' for k, v in data.items())

def send_notification(message: str):
    play_sound()
    run(['notify-send', '-a', 'Crypto Prices', f'{message}'])

def read_step_execute():
    with open('step.json', 'r') as file:
        data = json.load(file)
        step = data['step']
        
    if step % 2 == 0:
        symbols = ['ETH', 'POL', 'SFL']
        symbol_names = {'ETH': 'Ethereum', 'POL': 'POL (prev. MATIC)', 'SFL': 'Sunflower Land'}
    else:
        symbols = ['BTC', 'SOL', 'BNB']
        symbol_names = {'BTC': 'Bitcoin', 'SOL': 'Solana', 'BNB': 'BNB'}

    # Process and notify     
    prices = get_cleaned_prices(symbols, symbol_names)
    message = build_message(prices)
    send_notification(message)
    
    # Increment and save step
    data['step'] += 1
    with open('step.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    read_step_execute()