import os
from bottle import (get, post, redirect, request, route, run, static_file, template,
                    jinja2_view)
import utils
from functools import partial
import json
view = partial(jinja2_view, template_lookup=['templates'])

# Static Routes


@route('/browse')
@view('browse.tpl')
def browse_page():
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=[json.loads(utils.getJsonFromFile(elem)) for elem in utils.AVAILABLE_SHOWS])


@route('/ajax/show/<number>')
@view('show.tpl')
def browse_page(number):
    return template("./templates/show.tpl", version=utils.getVersion(),
                    result=json.loads(utils.getJsonFromFile(number)))

@route('/show/<number>')
@view('show.tpl')
def browse_page(number):
    sectionTemplate = "./templates/show.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=json.loads(utils.getJsonFromFile(number)))



@route('/search')
@view('search.tpl')
def search_page():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData={})


@post('/search')
@view('search.tpl')
def search_page():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=[json.loads(utils.getJsonFromFile(elem)) for elem in utils.AVAILABLE_SHOWS])


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
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


if _name_ == "_main_":
    run(host='localhost', port=7000, debug=True)