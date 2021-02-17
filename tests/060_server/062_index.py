import pytest

import cherrypy
from cherrypy.test import helper

from video_registry.serve import RegistryApplication, RegistryServer, Settings


@pytest.mark.usefixtures("server_settings_class")
class IndexViewTest(helper.CPWebCase):
    helper.CPWebCase.interactive = False

    @staticmethod
    def setup_server():
        # Static method cannot reach "self.server_settings" so we need to make
        # an identical Settings() instance with default values
        server = RegistryServer(Settings())

        cherrypy.tree.mount(
            RegistryApplication(server.settings),
            "",
            server.get_server_config(),
        )

    def test_index_page(self):
        """
        Server should return a success response for index mountpoint.
        """
        status, headers, body = self.getPage("/")
        self.assertStatus('200 OK')
