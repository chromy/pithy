from . import db

def create_link(url):
    l = Link()
    l.url = url
    db.session.add(l)
    db.session.flush()
    identifier = l.identifier = str(l.id)
    db.session.commit()
    return identifier

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(128))
    identifier = db.Column(db.String(12), unique=True)

    def __repr__(self):
        return '<Link({})>'.format(self.url)
