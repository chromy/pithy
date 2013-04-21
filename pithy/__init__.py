from flask import Flask, request, render_template, flash, redirect, \
    abort, url_for

app = Flask(__name__.split('.')[0])
app.secret_key = 'a'

URLS = {}

@app.route('/',  methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        short_url = shorten_link(request.form['url'])
        flash_short_url(short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_short_url(short_url):
    if short_url in URLS:
        return redirect(URLS[short_url], code=302)
    else:
        abort(404)

def shorten_link(url):
    short_url = str(hash(url))
    URLS[short_url] = url
    return short_url

def flash_short_url(short_url):
    link = url_for('redirect_short_url', short_url=short_url)
    s = 'Short url: <a href="{link}" class="short-link">{link}</a>'
    flash(s.format(link=link))

if __name__ == '__main__':
    app.run(debug=True)
