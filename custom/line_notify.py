import requests
from django.conf import settings

def send_text(message):
    url = 'https://notify-api.line.me/api/notify'
    headers = {
        'Authorization': f'Bearer {settings.LINE_NOTIFY_TOKEN}',
    }
    data = {
        'message': message,
    }
    response = requests.post(url, headers=headers, data=data)
    return response


def send_image(message, image_path):
    url = 'https://notify-api.line.me/api/notify'
    file = {'imageFile': open(image_path, 'rb')}
    headers = {
        'Authorization': f'Bearer {settings.LINE_NOTIFY_TOKEN}',
    }
    data = {
        'message': message,
    }
    session_post = requests.post(url, headers=headers, files=file, data=data)
    return session_post