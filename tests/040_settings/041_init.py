import os

import video_registry
from video_registry.serve import Settings


def test_init_default(test_settings):
    """
    Settings without arguments should use default values without any errors.
    """
    mixin = Settings()

    base_dir = os.path.abspath(
        os.path.dirname(video_registry.__file__)
    )

    assert mixin.HTTP_HOSTNAME == "0.0.0.0"
    assert mixin.HTTP_PORT == 8090
    assert mixin.STATIC_DIR == os.path.join(base_dir,
                                            mixin._default_assets_dirname)


def test_init_args(test_settings):
    """
    Settings with arguments should use given values without any errors.
    """
    mixin = Settings(
        hostname="localhost",
        port=90,
    )

    assert mixin.HTTP_HOSTNAME == "localhost"
    assert mixin.HTTP_PORT == 90
