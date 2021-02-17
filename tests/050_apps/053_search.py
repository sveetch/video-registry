import json


def test_search_view_all(db, server_app):
    """
    Dummy test to check view is returning a correct JSON response.
    """
    json_data = json.loads(server_app.search())

    assert json_data == {"todo": "todo"}

    #assert 1 == 42
