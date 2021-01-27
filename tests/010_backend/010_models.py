import logging

import pytest

from video_registry.backend.models import File


def test_model_file(caplog, db):
    """
    File model basic querysets should work without errors.
    """
    caplog.set_level(logging.DEBUG)

    foo = File.create(
        relative_path="foo/bar.mp4",
        absolute_path="/home/videos/foo/bar.mp4",
        basedir="/home/videos",
        extension="mp4",
        size=42,
    )

    tchi = File.create(
        relative_path="tchi/tcha.mpg",
        absolute_path="/home/videos/tchi/tcha.mpg",
        basedir="/home/videos",
        extension="mpg",
        size=712002,
    )

    ping = File.create(
        relative_path="ping/pong.mp4",
        absolute_path="/home/videos/ping/pong.mp4",
        basedir="/home/videos",
        extension="mp4",
        size=42,
    )

    assert File.select().count() == 3

    assert File.get_by_id(foo.id).relative_path == "foo/bar.mp4"
    assert File.get(File.relative_path == "foo/bar.mp4").size == 42

    assert File.select().where(File.size == 42).count() == 2
