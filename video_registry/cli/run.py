# -*- coding: utf-8 -*-
import logging

import click

from video_registry.discovery import VideoFileDiscovery
from video_registry.serve.server import RegistryServer


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
def run_command(context, directories):
    """
    Run a HTTP server to display discovered video files.
    """
    logger = logging.getLogger("video-registry")

    disco = VideoFileDiscovery()
    filepaths = disco.scan(directories)

    server = RegistryServer(
        "0.0.0.0",
        8090,
    )
    server.run()
