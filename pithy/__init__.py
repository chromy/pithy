from urlparse import urlparse
from flask import Flask, request, render_template, flash, redirect, \
    abort, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0])
app.secret_key = 'a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
from models import Link

@app.route('/',  methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form['url']
        short_url = shorten_link(url)
        flash_short_url(url, short_url)
    return render_template('index.html')

@app.route('/debug')
def debug():
    Link.create('http://www.hello.com')
    1/0

@app.route('/<identifier>')
def redirect_short_url(identifier):
    l = Link.get(identifier)
    if l:
        return redirect(l.url, code=302)
    else:
        abort(404)

def normalise_url(url):
    """Adds http to url if url has no protocol."""
    if urlparse(url).scheme == '':
        return 'http://' + url
    return url

def shorten_link(url):
    url = normalise_url(url)
    identifier = Link.create(url)
    return url_for('redirect_short_url', identifier=identifier, _external=True)

def flash_short_url(url, short_url):
    url_href = normalise_url(url)
    link = short_url.replace('http://', '')
    s = '<h2><a href="{}">{}</a> can now be found at \
        <a href="{}" class="short-link">{}</a></h2>'
    flash(s.format(url_href, url, short_url, link))
