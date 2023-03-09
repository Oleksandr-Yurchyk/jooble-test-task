import concurrent.futures
import logging

import flask
import requests as requests
from flask import Flask, request, make_response, jsonify

from .parser_helpers import get_request, parse_url, parse_domain, DomainData
from ..db import db

app = Flask(__name__)


@app.route('/endpoint1', methods=['POST'])
def post_endpoint1() -> flask.Response:
    url = request.json.get('url', [])
    db.create_db_table()

    urls = url if isinstance(url, list) else [url]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(parse_url, url) for url in urls]
        for f in concurrent.futures.as_completed(results):
            try:
                url_data = f.result()
            except requests.exceptions.RequestException as e:
                logging.error(f'The following error occurred --> {e}')
            else:
                db.insert_data(url_data)

    return make_response(jsonify(url_data), 200)


@app.route('/endpoint2', methods=['POST'])
def post_endpoint2() -> flask.Response:
    domain_name = request.json.get('domain_name', [])
    active_page_count = 0

    try:
        url_list = parse_domain(domain_name)
    except requests.exceptions.RequestException as e:
        logging.error(f'The following error occurred -> {e}')
        url_list = set()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(get_request, url) for url in url_list]
        for f in concurrent.futures.as_completed(results):
            try:
                response = f.result()
                if response.status_code == 200:
                    active_page_count += 1
            except requests.exceptions.RequestException as e:
                logging.error(f'The following error occurred -> {e}')

    domain_data: DomainData = {"active_page_count": active_page_count,
                               "total_page_count": len(url_list),
                               "url_list": list(url_list)}

    return make_response(jsonify(domain_data), 200)


if __name__ == '__main__':
    app.run()
