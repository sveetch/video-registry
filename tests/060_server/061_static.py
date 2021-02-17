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

    def test_static_mount(self):
        """
        Server should serve correctly assets for static mountpoint.
        """
        # Request for a special asset just for pinging
        url = "{}/ping.png".format(self.server_settings.STATIC_URL)
        status, headers, body = self.getPage(url)
        self.assertStatus('200 OK')
