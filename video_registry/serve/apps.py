import json

import cherrypy

from video_registry.renderer import JinjaRenderer


class ServerApp:
    """
    CherryPy Application for frontend and backend.

    TODO:
        * "/" : Index HTML page which will load assets and load frontend to
            display full list and perform search;
        * "/search/" : To receive search request to query Peewee backend;

    """
    def __init__(self, context):
        self.context = context
        self.renderer = JinjaRenderer(
            templates_dir=self.context["TEMPLATES_DIR"],
        )

    @cherrypy.expose
    def index(self):
        """
        Index HTML page.
        """

        content = self.renderer.render("index.html", {})
        return content

    @cherrypy.expose
    def search(self, length=8):
        """
        Backend response to search. Should it be used also to return the full
        list if no request query arguments ?
        """
        return json.dumps({"todo": "todo"})
