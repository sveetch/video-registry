import logging
import os

import cherrypy

import video_registry

from .apps import ServerApp


class RegistryServer:
    """
    Server to serve frontend, backend and static applications.

    Arguments:
        hostname (string): Newtwork Adress to bind on server.
        port (integer): Newtwork Port to bind on server

    Attributes:
        secure (boolean): Indicate server is running on HTTPS if ``True``.
            Default is ``False``, assume server is running on HTTP. This is
            currently only used to build server URL.
        log (logging): Logging object set to application "video-registry".
    """
    def __init__(self, hostname, port, secure=False):
        self.log = logging.getLogger("video-registry")
        self.hostname = hostname
        self.port = port
        self.secure = secure
        self.static_url = "/static"
        self.static_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(video_registry.__file__),
                "assets",
            )
        )
        self.templates_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(video_registry.__file__),
                "templates",
            )
        )

    def get_global_config(self):
        """
        Return the global server config.

        Returns:
            dict: Server configuration.
        """
        return {
            "server.socket_host": self.hostname,
            "server.socket_port": self.port,
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
            "tools.staticdir.dir": self.static_dir,
        }

    def get_server_config(self):
        """
        Return the full server config.

        Returns:
            dict: Server configuration.
        """
        return {
            "/": self.get_root_config(),
            self.static_url: self.get_static_app_config(),
        }

    def get_app_context(self):
        """
        Return context for main App.

        Returns:
            dict: Server configuration.
        """
        return {
            "STATIC_DIR": self.static_dir,
            "STATIC_URL": self.static_url,
            "TEMPLATES_DIR": self.templates_dir,
        }

    def run(self):
        """
        Run CherryPy instance on release.
        """
        msg = "Starting HTTP server on: {host}:{port}"
        self.log.info(msg.format(
            host=self.hostname,
            port=self.port
        ))

        self.log.warning("Use CTRL+C to terminate.")

        cherrypy.config.update(self.get_global_config())
        cherrypy.quickstart(
            ServerApp(self.get_app_context()),
            "",
            self.get_server_config(),
        )
