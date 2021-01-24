import pytest

import cherrypy
from cherrypy.test import helper

from video_registry.serve.apps import ServerApp
from video_registry.serve.server import RegistryServer


@pytest.mark.usefixtures("server_context_class")
class IndexViewTest(helper.CPWebCase):
    helper.CPWebCase.interactive = False

    @staticmethod
    def setup_server():
        server = RegistryServer("localhost", "8080")

        cherrypy.tree.mount(
            ServerApp(server.get_app_context()),
            "",
            server.get_server_config(),
        )

    def test_static_mount(self):
        """
        Server should serve correctly assets for static mountpoint.
        """
        # Request for a special asset just for pinging
        url = "{}/ping.png".format(self.server_context["STATIC_URL"])
        status, headers, body = self.getPage(url)
        self.assertStatus('200 OK')
