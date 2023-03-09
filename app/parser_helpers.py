from typing import TypedDict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
TIMEOUT = (3, 7)
URLData = TypedDict('URLData', {"final_url": str,
                                "final_status_code": int | None,
                                "status_code": int,
                                "title": str,
                                "domain_name": str})

DomainData = TypedDict('DomainData', {"active_page_count": int,
                                      "total_page_count": int,
                                      "url_list": list[str]})


def get_request(url: str, headers: dict = None, params: dict = None, timeout: int | tuple = 60) -> requests.Response:
    return requests.get(url, headers=headers, params=params, timeout=timeout)


def parse_url(url: str) -> dict:
    response = get_request(url, headers=HEADERS, timeout=TIMEOUT)

    final_status_code = None
    final_url = ''
    if response.history:
        for step in response.history:
            final_status_code = step.status_code
            final_url = step.url

    soup = BeautifulSoup(response.text, 'html.parser')
    domain_name = urlparse(url).netloc

    url_data: URLData = {
        "final_url": final_url,
        "final_status_code": final_status_code,
        "status_code": response.status_code,
        "title": soup.title.string if soup.title else '',
        "domain_name": domain_name,
    }
    return url_data


def parse_domain(domain: str) -> set:
    parsed_domain = urlparse(domain)
    url = f'https://{parsed_domain.path}' if not parsed_domain.scheme else ''

    response = get_request(url, headers=HEADERS, timeout=TIMEOUT)
    soup = BeautifulSoup(response.text, 'html.parser')

    url_list = [link.get('href') for link in soup.find_all('a')]
    return set(url_list)
