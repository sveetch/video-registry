import json

import pytest


def test_search_view_all(db, server_app):
    json_data = json.loads(server_app.search())

    assert json_data == {"todo": "todo"}

    #assert 1 == 42
