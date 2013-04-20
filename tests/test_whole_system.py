import pithy
from attest import Tests
system = Tests()

# Turn on testing.
pithy.app.config['TESTING'] = True

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

if __name__ == '__main__':
    system.run()
