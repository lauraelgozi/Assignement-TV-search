import os
from bottle import (get, post, redirect, request, route, run, static_file, template, TEMPLATE_PATH, jinja2_view, error)
import json
import utils
from functools import partial
TEMPLATE_PATH.insert(0, '')
view = partial(jinja2_view, template_lookup=['templates'])

# Static Routes



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


@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})



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


@route('/ajax/show/<number>')
@view('show.tpl')
def show(number):
    return template("./templates/show.tpl", version=utils.getVersion(),
                    result=json.loads(utils.getJsonFromFile(number)))


@route('/show/<number>')
@view("show.tpl")
def show(number):
    sectionTemplate = "./templates/show.tpl"
    return template("./pages/index.html", version=utils.getVersion(),
                    sectionTemplate=sectionTemplate,
                    sectionData=json.loads(utils.getJsonFromFile(number)))


@route('/show/<number>/episode/<id>')
@view("episode.tpl")
def episode(number, id):
    relevant_data = {}
    show = json.loads(utils.getJsonFromFile(number))
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if episode["id"] == int(id):
            relevant_data = episode
    sectionTemplate = "./templates/episode.tpl"
    return template("./pages/index.html", version=utils.getVersion(),
                    sectionTemplate=sectionTemplate,
                    sectionData=relevant_data)


@route('/ajax/show/<number>/episode/<id>')
@view("episode.tpl")
def episode(number, id):
    relevant_data = {}
    show = json.loads(utils.getJsonFromFile(number))
    episodes = show["_embedded"]["episodes"]
    for episode in episodes:
        if episode["id"] == int(id):
            relevant_data = episode
    return template("./templates/episode.tpl", result=relevant_data)


if __name__ == "__main__":
    run(host='localhost', port=7000, debug=True)
"""""
@route('/search', method="POST")
@view('search_result.tpl')
def search():
    search_word = request.forms.get("q")
    all_shows = [json.loads(utils.getJsonFromFile(show)) for show in utils.AVAILABLE_SHOWS]
    relevant_result = []
    for show in all_shows:
        for episode in show["_embedded"]["episodes"]:
            s = {}
            if type(episode['summary']) == str and search_word in episode['summary'] or type(episode['name']) == str and search_word in episode['name']:
                s["showid"] = show["id"]
                s['episodeid'] = episode["id"]
                s['text'] = show['name'] + " : " + episode["name"]
                relevant_result.append(s)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate="./templates/search_result.tpl",
                    sectionData={}, results = relevant_result, query = search_word)

@route('/search', method="POST")
@view('./templates/search_result.tpl')
def search_result():
    query = request.forms.get("q")
    for show in ALL_SHOWS:
        for episod in show["_embedded"]["episodes"]:
            for list in episod:
                if list == "summary":
                    if query in episod[list]:
                        text = episod[list]
                        print(episod["id"])
    results = [{
        "episodeid":"episodeid",
        'showid':'showid',
        'text':'text'
    }]
    return {'query': query,'results':results}

"""""