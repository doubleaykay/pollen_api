from flask import Flask, Response, jsonify, request
from requests_html import HTMLSession
from datetime import datetime as dt
import os
# import threading
import asyncio

from scraper import scrape_pollen_async

import nest_asyncio
nest_asyncio.apply()
# __import__('IPython').embed()

app = Flask(__name__)

@app.route('/')
def main():
    return 'You need a 🔑'

@app.route('/api', methods = ['GET'])
def get_data():

    # placeholder for key authorization
    key = 'hello'
    if key != 'hello':
        return 'You need a 🔑'

    zipcode = request.args.get('zipcode')

    # pollen_data = scrape_pollen_async(zipcode)

    loop = asyncio.new_event_loop()
    results = loop.run_until_complete(scrape_pollen_async(zipcode))

    # th = threading.Thread(target=scrape_pollen)
    # th.start()
    # pollen_data = scrape_pollen(zipcode)
    # th.join()

    return jsonify(results)
    # return Response(pollen_data)
    # return Response(results)


# run server
# if __name__ == '__main__':
#   app.run()
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host = '0.0.0.0', port = port)