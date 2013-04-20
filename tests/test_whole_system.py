import pithy
from attest import Tests
system = Tests()

@system.test
def should_greet_us():
    pithy.app.config['TESTING'] = True
    app = pithy.app.test_client()
    response = app.get('/')
    assert 'Hello World' in response.data

if __name__ == '__main__':
    system.run()
