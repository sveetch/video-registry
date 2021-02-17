import os

from py_css_styleguide.model import Manifest

from ..exceptions import StyleguideError


class StyleguideMixin:
    def get_manifest(self, path):
        """
        Open manifest file from given path, parse it and return a Styleguide
        manifest instance.

        Arguments:
            path (string): Absolute path to the built Styleguide manifest CSS
                file.

        Raises:
            StyleguideError: If unable to open or parse the manifest CSS file.

        Returns:
            py_css_styleguide.model.Manifest: Manifest instance.
        """
        if not os.path.exists(path):
            raise StyleguideError(
                "Unable to find manifest CSS file: {}".format(path)
            )

        manifest = Manifest()

        with open(path, 'r') as fp:
            manifest.load(fp)

        return manifest

    def manifest_to_dict(self, manifest):
        """
        A convenient helper to turn manifest content to a dict.

        This is something the manifest should implement in addition to its
        "to_json" method, in fact it should be the method that "to_json" should
        use to build its content.

        Arguments:
            manifest (py_css_styleguide.model.Manifest): Manifest instance.

        Returns:
            dict: Dictionnary of manifest rule attributes.
        """
        agregate = {
            'metas': manifest.metas,
        }

        agregate.update({k: getattr(manifest, k) for k in manifest._rule_attrs})

        return agregate
