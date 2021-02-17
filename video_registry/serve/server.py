import logging
import os

import cherrypy

import video_registry

from .apps import RegistryApplication
from .settings import Settings


class RegistryServer:
    """
    Application server to initialize configuration and run Application.

    Arguments:
        settings (video_registry.serve.settings.Settings): Settings object
            instance which contain every required settings and will be exposed
            in template context.

    Attributes:
        log (logging): Logging object set to application "video-registry".
    """
    def __init__(self, settings):
        self.log = logging.getLogger("video-registry")
        self.settings = settings

    def get_global_config(self):
        """
        Return the global server config.

        Returns:
            dict: Server configuration.
        """
        return {
            "server.socket_host": self.settings.HTTP_HOSTNAME,
            "server.socket_port": self.settings.HTTP_PORT,
            "engine.autoreload_on": False,
        }

    def get_root_config(self):
        """
        Return the root mountpoint config.

        Returns:
            dict: Server configuration.
        """
        return {
            "tools.gzip.on": True,
        }

    def get_static_app_config(self):
        """
        Return the static mountpoint config to set.

        Returns:
            dict: Application configuration.
        """
        return {
            #"tools.staticdir.index": "index.html",
            "tools.staticdir.on": True,
            "tools.staticdir.dir": self.settings.STATIC_DIR,
        }

    def get_server_config(self):
        """
        Return the full server config.

        Returns:
            dict: Server configuration.
        """
        return {
            "/": self.get_root_config(),
            self.settings.STATIC_URL: self.get_static_app_config(),
        }

    def run(self):
        """
        Run CherryPy instance on release.
        """
        msg = "Starting HTTP server on: {host}:{port}"
        self.log.info(msg.format(
            host=self.settings.HTTP_HOSTNAME,
            port=self.settings.HTTP_PORT
        ))

        self.log.warning("Use CTRL+C to terminate.")

        cherrypy.config.update(self.get_global_config())
        cherrypy.quickstart(
            RegistryApplication(self.settings),
            "",
            self.get_server_config(),
        )
