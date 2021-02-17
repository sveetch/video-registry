import logging
import os

from pathlib import Path

import pytest

from video_registry.discovery import VideoFileDiscovery
from video_registry.backend.models import File


@pytest.mark.parametrize("exts,expected", [
    (
        [
            "mp4",
            "flv",
        ],
        [
            ".mp4",
            ".flv",
            ".MP4",
            ".FLV",
        ],
    ),
    (
        [
            "mp4",
            "flv",
            "mpeg",
            ".foo.avi",
            "mp4",
            "mp4",
            "flv",
        ],
        [
            ".mp4",
            ".flv",
            ".mpeg",
            ".foo.avi",
            ".MP4",
            ".FLV",
            ".MPEG",
            ".FOO.AVI",
        ],
    ),
])
def test_get_video_extensions(exts, expected):
    """
    Should return all extensions with leading dot and uppercase versions.
    """
    disco = VideoFileDiscovery(video_extensions=exts)

    assert disco.get_video_extensions() == tuple(sorted(expected))


@pytest.mark.parametrize("filepath,basedir,expected", [
    (
        "{FIXTURES}/dummy-videos-dir/intro.mpg",
        "{FIXTURES}/dummy-videos-dir",
        {
            "absolute_path": "{FIXTURES}/dummy-videos-dir/intro.mpg",
            "basedir": "{FIXTURES}/dummy-videos-dir",
            "directory": "",
            "extension": "mpg",
            "filename": "intro",
            "relative_path": "intro.mpg",
            "size": 1,
        },
    ),
    (
        "{FIXTURES}/dummy-videos-dir/foo/simpsons_1.mp4",
        "{FIXTURES}",
        {
            "absolute_path": "{FIXTURES}/dummy-videos-dir/foo/simpsons_1.mp4",
            "basedir": "{FIXTURES}",
            "directory": "dummy-videos-dir/foo",
            "extension": "mp4",
            "filename": "simpsons_1",
            "relative_path": "dummy-videos-dir/foo/simpsons_1.mp4",
            "size": 2632,
        },
    ),
    (
        "{FIXTURES}/dummy-videos-dir/meow/pst-pst-pst/funny-rabbit.mov",
        "{FIXTURES}/dummy-videos-dir",
        {
            "absolute_path": "{FIXTURES}/dummy-videos-dir/meow/pst-pst-pst/funny-rabbit.mov",
            "basedir": "{FIXTURES}/dummy-videos-dir",
            "directory": "meow/pst-pst-pst",
            "extension": "mov",
            "filename": "funny-rabbit",
            "relative_path": "meow/pst-pst-pst/funny-rabbit.mov",
            "size": 8373,
        },
    ),
])
def test_format_file_item(caplog, test_settings, filepath, basedir, expected):
    """
    Method should return all informations for given file path.
    """
    caplog.set_level(logging.DEBUG)

    # Replace fixtures directory pattern with the right one
    filepath = test_settings.format(filepath)
    basedir = test_settings.format(basedir)
    expected["basedir"] = test_settings.format(expected["basedir"])
    expected["absolute_path"] = test_settings.format(expected["absolute_path"])

    disco = VideoFileDiscovery()

    path = Path(filepath)

    infos = disco.format_file_item(path, basedir)

    assert infos == expected


def test_scan_directory(test_settings):
    """
    A directory scanning should return every file informations
    according to file extension matching against allowed video extensions.
    """
    directory = os.path.join(test_settings.fixtures_path, "dummy-videos-dir")
    #directory = "/youdl/youdl/"
    # Mimic like we already know this file
    dummy_knowed = test_settings.format("{FIXTURES}/dummy-videos-dir/foo/simpsons_1.mp4")

    disco = VideoFileDiscovery()

    paths = disco.scan_directory(directory, knowed=[dummy_knowed])

    # Count expected matching files except the ones we already know
    assert len(paths) == 8

    # Ensure every item are Path objects
    assert len([item for item in paths if isinstance(item, dict)]) == 8


def test_scan(test_settings):
    """
    Batch scan should collect every file informations according to file
    extension matching from all directories and without duplication.
    """
    directories = [
        os.path.join(test_settings.fixtures_path, "dummy-videos-dir"),
        os.path.join(test_settings.fixtures_path, "another-dummy-dir"),
        os.path.join(test_settings.fixtures_path, "dummy-videos-dir/foo"),
    ]

    disco = VideoFileDiscovery()

    paths = disco.scan(directories)

    # Count expected matching files
    assert len(paths) == 11


def test_store(test_settings, db):
    """
    Every valid file should be stored.
    """
    directories = [
        os.path.join(test_settings.fixtures_path, "dummy-videos-dir"),
        os.path.join(test_settings.fixtures_path, "another-dummy-dir"),
        os.path.join(test_settings.fixtures_path, "dummy-videos-dir/foo"),
    ]

    disco = VideoFileDiscovery()

    paths = disco.store(directories)

    assert File.select().count() == 11
