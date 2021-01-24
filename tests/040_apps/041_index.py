import pytest

from video_registry.serve.apps import ServerApp
from video_registry.serve.server import RegistryServer

from tests.utils import html_pyquery


def test_index_view(server_app):
    body = server_app.index()

    dom = html_pyquery(body)

    # Check name is correct
    name = dom.find(".page-header__title")[0].text
    assert name == "Video Registry"
    name = dom.find(".page-content__title")[0].text
    assert name == "Video Registry"
