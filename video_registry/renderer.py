# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

import video_registry


class JinjaRenderer:
    """
    Build HTML page from template and context.

    Arguments:
        templates_dir (string): Path to directory which contains template files.
    """

    def __init__(self, *args, **kwargs):
        self.templates_dir = kwargs.pop("templates_dir")
        self.jinja_env = self.get_jinjaenv()

        super().__init__(*args, **kwargs)

    def get_jinjaenv(self):
        """
        Start Jinja environment.

        Returns:
            jinja2.Environment: Initialized Jinja environment.
        """
        env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(["html", "xml"])
        )
        return env

    def get_template(self, filepath):
        """
        Load and return Jinja template.

        Arguments:
            filepath (string): Filepath to the template from its registered
                location in Jinja environment.

        Returns:
            jinja2.Template: Template ready to render.
        """

        return self.jinja_env.get_template(filepath)

    def render(self, template_name, context):
        """
        Render document from given template and context.

        Arguments:
            template_name (string): Relative path from template directory.
            context (dict): Template context.

        Returns:
            string: Generated HTML content.
        """
        document = self.get_template(template_name)

        return document.render(
            **{
                "export": context,
            }
        )
