from requests_html import HTMLSession
from datetime import datetime as dt

# set zip code
# zipcode = '03755'

def scrape_pollen(zipcode, asynchr=False):
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