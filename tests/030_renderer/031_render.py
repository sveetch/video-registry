from video_registry.renderer import JinjaRenderer

from tests.utils import html_pyquery


def test_index(settings, server_context):
    """
    Index HTML page rendering.

    NOTE: This is dummy for now since there is no real page yet.
    """
    renderer = JinjaRenderer(
        templates_dir=server_context["TEMPLATES_DIR"],
    )

    content = renderer.render("index.html", {})

    dom = html_pyquery(content)

    # Check name is correct
    name = dom.find(".page-header__title")[0].text
    assert name == "Video Registry"
    name = dom.find(".page-content__title")[0].text
    assert name == "Video Registry"
