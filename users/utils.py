import telebot 
import random
import requests
API_TOKEN = '7143628618:AAHHyuHEyUePzIouOyrqfcdxmBXP_AD_ZEo'


def send_confirmation_code(chat_id):
    confirmation_code = ''.join(random.choices('0123456789', k=6))
    message = f'Your confirmation code: {confirmation_code}'
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, json=data)
    if not response.ok:
        print('Failed to send confirmation:', response.text)