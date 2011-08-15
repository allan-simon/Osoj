#!/usr/bin/python2.6
import sys
sys.path.insert(-1,"/usr/lib/pymodules/python2.6")

import web
from web import form
from test import Compiler
from Exercise import Exercise
from Freerun import Test
from Admin import *

urls = (
    '/', 'Index',
    '/exercise/(\\d*)', 'Exercise',
    '/admin/add-exercise', 'AddExo',
    '/admin/show-exercise/(\\d*)', 'ShowExo',
    '/freestyle', 'Test'
)
 
app = web.application(urls, globals())
 


class Index:

    def __init__(self) :
        self.db = web.database(dbn="sqlite", db="openoj.db")
        self.render = web.template.render('templates/', base = "layout")

    def GET(self):
        exosList = self.db.select(
            "exos",
            what = "id,title",
        );
        return self.render.index(exosList)


if __name__ == "__main__":
    app.run()
