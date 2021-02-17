import os
import json
from copy import deepcopy
from datetime import datetime

import cherrypy

from playhouse.shortcuts import model_to_dict

from ..backend.initialize import init_database
from ..backend.models import File, create_tables
from ..renderer import JinjaRenderer
from ..utils import CustomEncoder

from .mixins import StyleguideMixin


class RegistryApplication(StyleguideMixin):
    """
    CherryPy Application for backend.
    """
    def __init__(self, settings):
        self.settings = settings
        self.renderer = JinjaRenderer(
            templates_dir=self.settings.TEMPLATES_DIR,
        )

    def get_context(self, **kwargs):
        """
        Return context for template rendering.

        Context base is just the public settings.

        Arguments:
            **kwargs (dict): Additional context items.

        Returns:
            dict: Context items.
        """
        context = deepcopy(self.settings.to_dict())
        context.update(**kwargs)

        return context

    @cherrypy.expose
    def index(self):
        """
        Index page.
        """
        content = self.renderer.render("index.html", self.get_context())
        return content

    @cherrypy.expose
    def styleguide(self):
        """
        Styleguide page.
        """
        context = self.get_context()
        context["manifest"] = self.get_manifest(
            self.settings.STYLEGUIDE_MANIFEST_PATH
        )

        content = self.renderer.render("styleguide/index.html", context)
        return content

    @cherrypy.expose
    def prototype(self):
        """
        Interface prototyping page.
        """
        context = self.get_context()
        context["manifest"] = self.get_manifest(
            self.settings.STYLEGUIDE_MANIFEST_PATH
        )

        content = self.renderer.render("prototype/index.html", context)
        return content

    @cherrypy.expose
    def list(self, length=8):
        """
        Backend response to list every files.

        TODO:
            Bugged when used from the CLI (unknow with test since not covered
            yet). It seems CherryPy is working in its own thread or Bus system ?

            It results, the created db from CLI is not reachable from here.

            Simple solution may be to pass the db connector to RegistryApplication
            or RegistryServer, however i don't know to use it with model
            queryset as below.

            CherryPy document some workaround with listener/sender to its Bus
            system but it's not totally concretly clear.
        """
        items = []

        for item in File.select():
            items.append(model_to_dict(item))

        return json.dumps(items, cls=CustomEncoder)

    @cherrypy.expose
    def search(self, length=8):
        """
        TODO:
            Backend response to search pattern ? Or cancel backend search
            feature in profit of basic frontend search ?
        """
        return json.dumps({"todo": "todo"})
