def test_get_app_context(server_app):
    context = server_app.get_context()

    # Just check presence of some base settings
    assert ("HTTP_HOSTNAME" in context) is True
    assert ("HTTP_PORT" in context) is True
    assert ("STATIC_URL" in context) is True
    assert ("TEMPLATES_DIR" in context) is True

