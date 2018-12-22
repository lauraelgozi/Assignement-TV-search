import os
from bottle import (get, request, route, run, static_file, template, TEMPLATE_PATH, jinja2_view, error)
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
                    sectionData=[json.loads(utils.getJsonFromFile(movie)) for movie in utils.AVAILABE_SHOWS])


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



@route('/search')
@view('search.tpl')
def search_page():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/search', method="POST")
@view('search_result.tpl')
def search_page():
    user_input = request.forms.get("q")
    shows_list = []
    for show in utils.AVAILABE_SHOWS:
        shows_list.append(json.loads(utils.getJsonFromFile(show)))
    relevant_episode = []
    for show in shows_list:
        for episode in show["_embedded"]["episodes"]:
            r = {}
            if type(episode['summary']) == str and user_input in episode['summary'] or type(episode['name']) == str and user_input in episode['name']:
                r["showid"] = show["id"]
                r['episodeid'] = episode["id"]
                r['text'] = show['name'] + " : " + episode["name"]
                relevant_episode.append(r)
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate="./templates/search_result.tpl",
                    sectionData={}, results=relevant_episode, query=user_input)





if __name__ == "__main__":
    run(host='localhost', port=7000, debug=True)
