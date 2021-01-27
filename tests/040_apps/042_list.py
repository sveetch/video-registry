import json
import os

import pytest

from video_registry.discovery import VideoFileDiscovery


def test_search_view_all(settings, db, server_app):
    directories = [
        os.path.join(settings.fixtures_path, "dummy-videos-dir"),
        os.path.join(settings.fixtures_path, "another-dummy-dir"),
        os.path.join(settings.fixtures_path, "dummy-videos-dir/foo"),
    ]

    disco = VideoFileDiscovery()

    paths = disco.store(directories)
    json_data = json.loads(server_app.list())

    assert len(json_data) == 11

    first = json_data[0]

    assert list(first.keys()) == [
        "id",
        "created",
        "absolute_path",
        "relative_path",
        "basedir",
        "extension",
        "size",
    ]
