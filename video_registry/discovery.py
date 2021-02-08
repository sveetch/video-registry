"""
Discovering
===========

"""
import logging
import os

from pathlib import Path

from video_registry.backend.models import File


class VideoFileDiscovery:
    """
    Discovery video file from directory scanning.

    Keyword Arguments:
        name (str): Define a custom name to greet if given.

    Attributes:
        name (str): Name to greet, default to ``world``.
    """
    VIDEO_EXTENSIONS = [
        "mp4",
        "flv",
        "mov",
        "mpg",
        "mpeg",
        "avi",
    ]

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger("video-registry")
        self.video_extensions = kwargs.get("video_extensions") or self.VIDEO_EXTENSIONS

    def get_video_extensions(self):
        """
        Return allowed file extension to search as video files.

        Arguments:
            directory (string): Directory filepath.

        Returns:
            tuple: Tuple of every extension with leading dot (if extension don't
            already have it) and uppercase version.
        """
        exts = set([])

        for item in self.video_extensions:
            if item.startswith("."):
                ext = item
            else:
                ext = ".{}".format(item)

            exts.add(ext)
            exts.add(ext.upper())

        return tuple(sorted(exts))

    def format_file_item(self, path, basedir):
        """
        Return computed informations from given Path.

        Arguments:
            path (pathlib.Path): A path object to a file (path to a directory is
                not supported). It is assumed than path is always correct,
                meaning it does exists and is a file and it should be resolved
                (as with ``Path.resolve()``).
            basedir (string): Base directory as given to
                ``VideoFileDiscovery.scan_directory``.

        Returns:
            dict: A dict of informations about path.
        """
        filename = ".".join(path.name.split(".")[0:-1])
        extension = path.suffix[1:] if path.suffix.startswith(".") else path.suffix
        # Get resolved relative path
        rel_path = path.relative_to(basedir)
        # Prefer empty string instead of "." for parent resolution
        parent = str(rel_path.parent)
        parent = "" if parent == "." else parent

        infos = {
            "absolute_path": str(path),
            "relative_path": str(rel_path),
            "directory": parent,
            "filename": filename,
            "extension": extension,
            "size": path.stat().st_size,
            "basedir": basedir,
        }

        return infos

    def scan_directory(self, directory, knowed=[]):
        """
        Scan given directory to search for files or possible sub directories.

        Arguments:
            directory (string): Directory filepath. It should be an absolute
                path.

        Keyword Arguments:
            knowed (list): A list of knowed absolute file paths (as strings)
                used to ignore already discovered identical files.

        Returns:
            list: A list of ``pathlib.Path``.
        """
        self.logger.info("Scanning: {}".format(directory))

        dirpath = Path(directory)

        items = []

        for item in dirpath.glob('**/*'):
            if str(item).endswith(self.get_video_extensions()):
                infos = self.format_file_item(item, str(dirpath))
                if infos["absolute_path"] not in knowed:
                    items.append(infos)
                    knowed.append(infos["absolute_path"])

        return items

    def scan(self, directories):
        """
        Scan all given directories.

        Arguments:
            directories (list): List of directory paths to scan.

        Returns:
            list: List of all discovered file informations. List is assured to
            not register the same file twice for different given base
            directories such as for given "/foo/bar" and "/foo",
            "foo/bar/plop.mp4" won't be stored twice.
        """
        filepaths = []
        knowed = []

        for directory in directories:
            filepaths.extend(
                self.scan_directory(directory, knowed=knowed)
            )

        return filepaths

    def store(self, directories):
        """
        Scan and store retrieved paths.

        Arguments:
            directories (list): List of directory paths to scan.
        """
        filepaths = self.scan(directories)

        for item in filepaths:
            ping = File.create(
                relative_path=item["relative_path"],
                absolute_path=item["absolute_path"],
                basedir=item["basedir"],
                extension=item["extension"],
                size=item["size"],
            )

        return filepaths
