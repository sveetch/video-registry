import logging

import pytest

from video_registry.backend.models import File


def test_model_file(caplog, db):
    """
    File model basic querysets should work without errors.
    """
    caplog.set_level(logging.DEBUG)

    foo = File.create(
        path="foo/bar.mp4",
        size=42,
    )

    tchi = File.create(
        path="tchi/tcha.mpg",
        size=712002,
    )

    ping = File.create(
        path="ping/pong.mp4",
        size=42,
    )

    assert File.select().count() == 3

    assert File.get_by_id(foo.id).path == "foo/bar.mp4"
    assert File.get(File.path == "foo/bar.mp4").size == 42

    assert File.select().where(File.size == 42).count() == 2
