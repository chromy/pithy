import pithy
from flask import redirect

from bs4 import BeautifulSoup
from attest import Tests
system = Tests()

# Turn on testing.
pithy.app.config['TESTING'] = True

def extract_short_url(data):
    soup = BeautifulSoup(data)
    links = soup.findAll('a', {'class':'short-link'})
    assert len(links) == 1
    return links[0].get_text()

@system.context
def connect():
    app = pithy.app.test_client()
    try:
        yield app
    finally:
        pass

@system.test
def should_greet_us(app):
    response = app.get('/')
    assert 'Hello World' in response.data

@system.test
def should_shorten_url(app):
    response = app.post('/', data={'url':'http://www.example.com'})
    short_url = extract_short_url(response.data)
    response = app.get(short_url)
    assert response.status_code == 302
    assert response.location == 'http://www.example.com'

@system.test
def should_404_unused_short_urls(app):
    response = app.get('/abcde')
    assert response.status_code == 404

if __name__ == '__main__':
    system.run()
