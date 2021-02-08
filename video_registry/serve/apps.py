import os
import json
from datetime import datetime

import cherrypy

from playhouse.shortcuts import model_to_dict

from video_registry.backend.initialize import init_database
from video_registry.backend.models import File, create_tables
from video_registry.renderer import JinjaRenderer
from video_registry.utils import CustomEncoder



class ServerApp:
    # Path to CSS manifest to parse from Styleguide app
    STYLEGUIDE_MANIFEST_PATH = os.path.join(
        'css',
        'styleguide_manifest.css'
    )

    """
    CherryPy Application for frontend and backend.
    """
    def __init__(self, context):
        self.context = context
        self.renderer = JinjaRenderer(
            templates_dir=self.context["TEMPLATES_DIR"],
        )

    @cherrypy.expose
    def index(self):
        """
        Index page.
        """
        content = self.renderer.render("index.html", self.context)
        return content

    @cherrypy.expose
    def styleguide(self):
        """
        Styleguide page.

        TODO:
            Include code to build page context with styleguide using
            py_css_styleguide
        """
        content = self.renderer.render("styleguide/index.html", self.context)
        return content

    @cherrypy.expose
    def list(self, length=8):
        """
        Backend response to list every files.
        """
        items = []

        for item in File.select():
            items.append(model_to_dict(item))

        return json.dumps(items, cls=CustomEncoder)

    @cherrypy.expose
    def search(self, length=8):
        """
        TODO: Backend response to search pattern ?
        """
        return json.dumps({"todo": "todo"})
