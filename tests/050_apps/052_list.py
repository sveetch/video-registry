import json
import os

from video_registry.discovery import VideoFileDiscovery


def test_list_view_all(test_settings, db, server_app):
    """
    View should return JSON data for discovered files.
    """
    directories = [
        os.path.join(test_settings.fixtures_path, "dummy-videos-dir"),
        os.path.join(test_settings.fixtures_path, "another-dummy-dir"),
        os.path.join(test_settings.fixtures_path, "dummy-videos-dir/foo"),
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
