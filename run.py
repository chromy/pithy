#! /usr/bin/env python

from pithy import app, db

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.debug = True
    app.run()
