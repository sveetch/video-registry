from video_registry.serve import Settings


def test_to_dict(test_settings):
    """
    Method should return all available settings.
    """
    mixin = Settings()
    mixin.foo = "bar"
    mixin._PLOP = "PLIP"

    names = mixin.to_dict()

    assert ("foo" not in names) is True
    assert ("_PLOP" not in names) is True
    assert ("HTTP_HOSTNAME" in names) is True
