import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
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

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls


def crawl(site_id, url):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > 100:
            for l in internal_urls:
                print(site_id, l)
                data = {
                    'site_id': site_id,
                    'link': l
                }
                message = json.dumps(data)
                rmq_channel.basic_publish(exchange=exchange_, routing_key="tests", body=message)
            exit('Scanning completed')
        else:
            crawl(site_id, link)


# if __name__ == "__main__":
#     import argparse
#
#     parser = argparse.ArgumentParser(description="Link Extractor Tool with Python")
#     parser.add_argument("url", help="The URL to extract links from.")
#
#     args = parser.parse_args()
#     url = args.url
#
#     crawl(url)
#
#     print("[+] Total Internal links:", len(internal_urls))
#     print("[+] Total External links:", len(external_urls))
#     print("[+] Total URLs:", len(external_urls) + len(internal_urls))
#
#     domain_name = urlparse(url).netloc
#
#     # save the internal links to a file
#     with open(f"{domain_name}_internal_links.txt", "w") as f:
#         for internal_link in internal_urls:
#             print(internal_link.strip(), file=f)
#
#     # save the external links to a file
#     with open(f"{domain_name}_external_links.txt", "w") as f:
#         for external_link in external_urls:
#             print(external_link.strip(), file=f)
