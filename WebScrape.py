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

    Source: https://realpython.com/python-web-scraping-practical-introduction/

    """

    try:
        with closing(get(url, stream=True)) as resp:  # stream=True will download headers only first
            if is_good_response(resp):  # checks if HTML
                return resp.content  # HTML page content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.

    Source: https://realpython.com/python-web-scraping-practical-introduction/

    """

    content_type = resp.headers['Content-Type'].lower()  # check headers, make them lower case
    return (resp.status_code == 200  # this is a good code
            and content_type is not None
            and content_type.find('html') > -1)  # checks that it's an HTML page


def log_error(e):
    """
    Print errors

    Source: https://realpython.com/python-web-scraping-practical-introduction/

    """
    print(e)


raw_html = simple_get('https://www.audible.com/special-promo/2for1/cat?ref=a_special-p_l1_catRefs_0&searchCategory=211&ref=a_special-p_c2_showmore&pf_rd_p=2aa65428-a2ee-47af-abab-dbefbc452d55&pf_rd_r=GQK6YWTSF6QVGSZGH1FG&')
html = BeautifulSoup(raw_html, 'html.parser')
print(html)