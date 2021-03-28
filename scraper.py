from requests_html import HTMLSession
from datetime import datetime as dt

from requests_html import AsyncHTMLSession
import pyppeteer

# set zip code
# zipcode = '03755'

def scrape_pollen(zipcode):
    """
    Function to scrape pollen data from Pollen.com
    Returns JSON with pollen data and timestamp (for validation/debugging)
    """
    # note timestamp
    timestamp = dt.now().strftime("%m/%d/%Y, %H:%M:%S")

    # get page
    session = HTMLSession()
    r = session.get('https://www.pollen.com/forecast/current/pollen/' + zipcode)

    # find html tags with pollen data in them
    r.html.render()
    data = r.html.find('#today > p.forecast-level.ng-binding')
    yesterday_html = data[0].html
    today_html = data[1].html
    tomorrow_html = data[2].html

    # split paragraph tags to get data contained within
    yesterday = yesterday_html.split('>')[1].split('<')[0]
    today = today_html.split('>')[1].split('<')[0]
    tomorrow = tomorrow_html.split('>')[1].split('<')[0]

    # pack everything into JSON
    pollen_data = {
        'timestamp': timestamp,
        'yesterday': yesterday,
        'today': today,
        'tomorrow': tomorrow
    }

    return pollen_data

async def scrape_pollen_async(zipcode):
    """
    Function to scrape pollen data from Pollen.com
    Returns JSON with pollen data and timestamp (for validation/debugging)
    """

    # fixed AsyncHTMLSession as per https://github.com/psf/requests-html/issues/293
    class AsyncHTMLSessionFixed(AsyncHTMLSession):
        """
        pip3 install websockets==6.0 --force-reinstall
        """
        def __init__(self, **kwargs):
            super(AsyncHTMLSessionFixed, self).__init__(**kwargs)
            self.__browser_args = kwargs.get("browser_args", ["--no-sandbox"])

        @property
        async def browser(self):
            if not hasattr(self, "_browser"):
                self._browser = await pyppeteer.launch(ignoreHTTPSErrors=not(self.verify), headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, args=self.__browser_args)

            return self._browser

    # note timestamp
    timestamp = dt.now().strftime("%m/%d/%Y, %H:%M:%S")

    # get page
    asession = AsyncHTMLSessionFixed()
    r = await asession.get('https://www.pollen.com/forecast/current/pollen/' + zipcode)

    # find html tags with pollen data in them
    await r.html.arender()
    data = r.html.find('#today > p.forecast-level.ng-binding')
    yesterday_html = data[0].html
    today_html = data[1].html
    tomorrow_html = data[2].html

    # split paragraph tags to get data contained within
    yesterday = yesterday_html.split('>')[1].split('<')[0]
    today = today_html.split('>')[1].split('<')[0]
    tomorrow = tomorrow_html.split('>')[1].split('<')[0]

    # pack everything into JSON
    pollen_data = {
        'timestamp': timestamp,
        'yesterday': yesterday,
        'today': today,
        'tomorrow': tomorrow
    }

    return pollen_data