import pytest

import cherrypy
from cherrypy.test import helper

from video_registry.serve.apps import ServerApp
from video_registry.serve.server import RegistryServer


@pytest.mark.usefixtures("server_context_class")
class SearchViewTest(helper.CPWebCase):
    helper.CPWebCase.interactive = False

    @staticmethod
    def setup_server():
        server = RegistryServer("localhost", "8080")

        cherrypy.tree.mount(
            ServerApp(server.get_app_context()),
            "",
            server.get_server_config(),
        )

    def test_search_page(self):
        """
        Server should return a success response for search mountpoint.
        """
        self.getPage("/search")
        self.assertStatus('200 OK')
