import requests
#from requests import get
#from requests import post
#from requests import session
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import config #you must update the config.py with your Audible Amazon account information before the script will work.

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

#Source: https://pybit.es/requests-session.html
#Source: http://theautomatic.net/2017/08/19/logging-into-amazon-with-python/

#Request URL - page I want to scrape
getURL = 'https://www.audible.com/ep/DD-Resale'

#define URL where login form is located
loginURL = 'https://www.amazon.com/gp/sign-in.html'

#initiate session
session = requests.Session()

#define session headers
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': loginURL
}

#get login page
resp = session.get(loginURL)
html = resp.text

#get BeautifulSoup object of the html of the login page
soup = BeautifulSoup(html, 'lxml')

#scrape login page to get all the needed inputs required for login
data = {}
form = soup.find('form', {'name': 'signIn'})
for field in form.find_all('input'):
    try:
        data[field['name']] = field['value']

    except:
        pass

#add username and password to the data for post request
data[u'email'] = config.email
data[u'password'] = config.password

i=1

while i < 6:
    # submit post request with username / password and other needed info
    post_resp = session.post('https://www.amazon.com/ap/signin/;', data=data)
    post_soup = BeautifulSoup(post_resp.content, 'lxml')

    if post_soup.find_all('title')[0].text == 'Your Account':
        print('Login Successful')
        break
    elif i == 5:
        print('Login Failed')
        break
    else:
        print('Login In Progress')
        i += 1

raw = session.get(getURL)
html = raw.content
soup = BeautifulSoup(html, 'html.parser').encode("utf-8")
#print(soup)

session.close()


