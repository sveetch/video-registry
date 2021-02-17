# -*- coding: utf-8 -*-
import logging

import click

from ..backend.initialize import init_database
from ..backend.models import File
from ..discovery import VideoFileDiscovery
from ..serve import RegistryServer, Settings


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

    db = init_database()
    db.create_tables([File])

    disco = VideoFileDiscovery()
    filepaths = disco.store(directories)

    settings = Settings(
        hostname="0.0.0.0",
        port=8090,
    )

    server = RegistryServer(settings)
    server.run()

    #db.close()
