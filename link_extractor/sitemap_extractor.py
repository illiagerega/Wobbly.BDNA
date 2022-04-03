from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import pika
import sys
import os
import json

sys.path.insert(0, os.path.abspath(''))

import config

# params for RabbitMQ
queue_ = config.rmq_queue
exchange_ = 'links_'

rmq_parameters = pika.URLParameters(f'amqp://{config.rmq_user}:{config.rmq_password}@{config.rmq_host}:{config.rmq_port}')
rmq_connection = pika.BlockingConnection(rmq_parameters)
rmq_channel = rmq_connection.channel()

rmq_channel.exchange_declare(exchange_)
rmq_channel.queue_declare(queue=queue_, durable=True)
rmq_channel.queue_bind(queue_, exchange_, "tests")


def get_sitemap(url):
    get_url = requests.get(url)

    if get_url.status_code == 200:
        return get_url.text
    else:
        print('Unable to fetch sitemap: %s.' % url)


def process_sitemap(s):
    soup = BeautifulSoup(s, 'lxml')
    result = []

    for loc in soup.findAll('loc'):
        result.append(loc.text)

    return result


def is_sub_sitemap(url):
    parts = urlparse(url)
    if parts.path.endswith('.xml') and 'sitemap' in parts.path:
        return True
    else:
        return False


def parse_sitemap(s):
    try:
        sitemap = process_sitemap(s)
        result = []

        while sitemap:
            candidate = sitemap.pop()

            if is_sub_sitemap(candidate):
                sub_sitemap = get_sitemap(candidate)
                for i in process_sitemap(sub_sitemap):
                    sitemap.append(i)
            else:
                result.append(candidate)

        return result
    except:
        return False


def main(site_id, sitemap_):
    sitemap = get_sitemap(sitemap_)

    if sitemap:
        for url in parse_sitemap(sitemap):
            data = {
                'site_id': site_id,
                'link': url
            }
            message = json.dumps(data)

            rmq_channel.basic_publish(exchange=exchange_, routing_key="tests", body=message)
    else:
        print('Bad sitemap')


# if __name__ == '__main__':
#     main()
