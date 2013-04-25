from flask import Flask, request, render_template, flash, redirect, \
    abort, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__.split('.')[0])
app.secret_key = 'a'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
from models import create_link, Link

URLS = {}

@app.route('/',  methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        short_url = shorten_link(request.form['url'])
        flash_short_url(short_url)
    return render_template('index.html')

@app.route('/debug')
def debug():
    create_link('http://www.hello.com')
    1/0

@app.route('/<identifier>')
def redirect_short_url(identifier):
    l = Link.query.filter_by(identifier=identifier).first()
    if l:
        return redirect(l.url, code=302)
    else:
        abort(404)

def shorten_link(url):
    identifier = create_link(url)
    return url_for('redirect_short_url', identifier=identifier)

def flash_short_url(short_url):
    s = 'Short url: <a href="{link}" class="short-link">{link}</a>'
    flash(s.format(link=short_url))
