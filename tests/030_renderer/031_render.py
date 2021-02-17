from video_registry.renderer import JinjaRenderer

from tests.utils import html_pyquery


def test_index(server_settings):
    """
    Renderer should correctly build the page document from template without
    any errors.
    """
    renderer = JinjaRenderer(
        templates_dir=server_settings.TEMPLATES_DIR,
    )

    content = renderer.render("index.html", {})

    dom = html_pyquery(content)

    # Check name is correct
    name = dom.find(".page-header__title")[0].text
    assert name == "Video Registry"
    name = dom.find(".page-content__title")[0].text
    assert name == "Video Registry"
