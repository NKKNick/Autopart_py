import requests
from django.conf import settings

def send_line_notification(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {settings.LINE_NOTIFY_TOKEN}',
    }
    data = {
        'message': message,
    }
    response = requests.post(url, headers=headers, data=data)
    return response