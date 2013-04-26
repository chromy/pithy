from flask import Flask, request, render_template, flash, redirect, \
    abort, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0])
app.secret_key = 'a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
from models import Link

URLS = {}

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

def shorten_link(url):
    identifier = Link.create(url)
    return url_for('redirect_short_url', identifier=identifier, _external=True)

def flash_short_url(url, short_url):
    s = '<a href="{url}">{url}</a> \
        <a href="{short_url}" class="short-link">{short_url}</a>'
    flash(s.format(url=url, short_url=short_url))
