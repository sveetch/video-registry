# -*- coding: utf-8 -*-
import click

from video_registry import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo("video-registry {}".format(__version__))
