import requests
from bs4 import BeautifulSoup
import pika
import sys
import os
import json

import db

sys.path.insert(0, os.path.abspath(''))

import config

queue_ = config.rmq_queue

rmq_parameters = pika.URLParameters(
    f'amqp://{config.rmq_user}:{config.rmq_password}@{config.rmq_host}:{config.rmq_port}')
rmq_connection = pika.BlockingConnection(rmq_parameters)
rmq_channel = rmq_connection.channel()

rmq_channel.queue_declare(queue=queue_, durable=True)


def on_message(channel, method_frame, header_frame, body):
    data = json.loads(body)
    print(data['site_id'], data['link'])

    res = requests.get(data['link'])
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'footer',
        'iframe',
        'section',
        'style'
        # there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        # if re.match('<!--.*-->', str(element.encode('utf-8'))):
        #     continue
        if t.parent.name not in blacklist:
            output += '{} '.format(t)

    text = " ".join(output.split())
    text_ = text.replace("'", "")

    if db.checkLink(data['link'])[0] != 1:
        db.insertLink(data['link'], data['site_id'], text_)
    else:
        print('link already exists')

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


rmq_channel.basic_consume(queue_, on_message)
rmq_channel.start_consuming()

# try:
#     rmq_channel.start_consuming()
# except KeyboardInterrupt:
#     rmq_channel.stop_consuming()
# rmq_connection.close()