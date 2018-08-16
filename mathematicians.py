from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.

    Function will "try" to call URL "except" if it throws a RequestException error,
    which it will log. If no error, it will check that it is an HTML page with
    is_good_response() and then return content if all is good.

    Source: https://realpython.com/python-web-scraping-practical-introduction/#wrangling-html-with-beautifulsoup

    """

    try:
        with closing(get(url, stream=True)) as resp: #stream=True will download headers only first
            if is_good_response(resp): #checks if HTML
                return resp.content #HTML page content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """

    content_type = resp.headers['Content-Type'].lower() #check headers, make them lower case
    return (resp.status_code == 200 #this is a good code
            and content_type is not None
            and content_type.find('html') > -1) #checks that it's an HTML page


def log_error(e):
    """
    Print errors

    """
    print(e)

raw_html = simple_get('http://www.fabpedigree.com/james/mathmen.htm')
html = BeautifulSoup(raw_html, 'html.parser')
for i, li in enumerate(html.select('li')):
        print(i, li.text)