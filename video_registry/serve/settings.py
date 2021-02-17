import os
import logging

import video_registry


class Settings:
    """
    Settings object to define and store every setting for server and
    application.

    Keyword Arguments:
        hostname (string): Newtwork Adress to bind on server. Default to
            ``0.0.0.0`` (listen on all interfaces).
        port (integer): Newtwork Port to bind on server. Default to ``8090``.
        secure (boolean): Indicate server is running on HTTPS if ``True``.
            Default is ``False``, assume server is running on HTTP. This is
            currently only used to build server URL.

    Attributes:
        log (logging): Logging object set to application "video-registry".
    """
    _default_hostname = "0.0.0.0"
    _default_port = 8090
    _default_static_endpoint = "static"
    _default_assets_dirname = "assets"
    _default_templates_dirname = "templates"

    def __init__(self, hostname=None, port=None, secure=False):
        self.log = logging.getLogger("video-registry")

        # Server network interface
        self.HTTP_HOSTNAME = hostname or self._default_hostname
        self.HTTP_PORT = port or self._default_port
        self.HTTP_SECURE = secure

        # Base directory to the module
        self.BASE_DIR = os.path.abspath(
            os.path.dirname(video_registry.__file__)
        )

        # Static files
        self.STATIC_URL = "/" + self._default_static_endpoint
        self.STATIC_DIR = os.path.join(
            self.BASE_DIR,
            self._default_assets_dirname
        )

        # Template directory
        self.TEMPLATES_DIR = os.path.join(
            self.BASE_DIR,
            self._default_templates_dirname
        )

        # Styleguide
        self.STYLEGUIDE_MANIFEST_PATH = os.path.join(
            self.STATIC_DIR,
            "css",
            "styleguide_manifest.css"
        )

    def to_dict(self):
        """
        Return every settings in a dictionnary.

        A exposed setting is an object attribute with a name in uppercase and
        that does not start with ``_``.
        """
        return {
            k: v for k, v in vars(self).items()
            if (k.isupper() and not k.startswith("_"))
        }
