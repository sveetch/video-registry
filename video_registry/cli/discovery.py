# -*- coding: utf-8 -*-
import logging

import click

from video_registry.discovery import VideoFileDiscovery


@click.command()
@click.argument(
    "directories",
    type=click.Path(
        exists=True,
        resolve_path=True,
        file_okay=False,
    ),
    nargs=-1,
    required=True
)
@click.pass_context
def discovery_command(context, directories):
    """
    Scan given directories to find all Video files
    """
    logger = logging.getLogger("video-registry")

    disco = VideoFileDiscovery()
    filepaths = disco.scan(directories)

    import json

    print(
        json.dumps(filepaths, indent=4)
    )

    click.echo("{} item(s). Done.".format(len(filepaths)))
