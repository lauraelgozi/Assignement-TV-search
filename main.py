import os
from bottle import (get, post, redirect, request, route, run, static_file, template, TEMPLATE_PATH, error)
import json
from functools import partial

TEMPLATE_PATH.insert(0, '')
import utils

# Static Routes


@error(404)
def error404(error):
    return template("404.tpl")


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


@route('/browse')
def index():
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(),
                    sectionTemplate=sectionTemplate,
                    sectionData=[json.loads(utils.getJsonFromFile(elem)) for elem in utils.AVAILABE_SHOWS])


@route('/search')
def index():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData = {})


if __name__ == "__main__":
    run(host='localhost', port=7000, debug=True)
