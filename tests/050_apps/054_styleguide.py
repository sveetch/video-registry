import pytest

from tests.utils import html_pyquery

from video_registry.serve import StyleguideMixin, Settings

from video_registry.exceptions import StyleguideError


def test_get_manifest_error(test_settings):
    """
    Method should raise a StyleguideError when unable to open file.
    """
    mixin = StyleguideMixin()
    mixin.settings = Settings()

    with pytest.raises(StyleguideError):
        manifest = mixin.get_manifest("nope")


def test_get_manifest(test_settings):
    """
    Method should find manifest and parse it correctly.
    """
    mixin = StyleguideMixin()
    mixin.settings = Settings()

    # Open and parse manifest
    manifest = mixin.get_manifest(
        mixin.settings.STYLEGUIDE_MANIFEST_PATH
    )

    # Ensure manifest has finded some references at it should be
    assert len(manifest.metas) > 0
    assert ("references" in manifest.metas) is True
    assert len(manifest.metas["references"]) > 0

    for item in manifest.metas["references"]:
        assert hasattr(manifest, item) is True


def test_manifest_to_dict(test_settings):
    """
    Method should return a correct dict for all rules from manifest.
    """
    mixin = StyleguideMixin()
    mixin.settings = Settings()

    # Open and parse manifest
    manifest = mixin.get_manifest(
        mixin.settings.STYLEGUIDE_MANIFEST_PATH
    )

    # Turn manifest rule attributes to a dict
    content = mixin.manifest_to_dict(manifest)

    # Ensure manifest has finded some references at it should be
    assert ("metas" in content) is True
    assert ("references" in content["metas"]) is True

    for item in content["metas"]["references"]:
        assert (item in content) is True


def test_styleguide_view(server_app):
    body = server_app.styleguide()

    dom = html_pyquery(body)

    # Check name is correct
    name = dom.find(".page-header__title")[0].text
    assert name == "Video Registry"
    name = dom.find(".page-content__title")[0].text
    assert name == "Styleguide"
