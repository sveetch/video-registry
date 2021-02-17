"""
Pytest fixtures
"""
import logging
import os

import pytest

import video_registry

from video_registry.backend.initialize import init_database
from video_registry.backend.models import Dummy, File
from video_registry.serve import RegistryApplication, RegistryServer, Settings


class FixturesSettingsTestMixin(object):
    """
    A mixin containing settings about application. This is almost about useful
    paths which may be used in tests.

    Attributes:
        application_path (str): Absolute path to the application directory.
        package_path (str): Absolute path to the package directory.
        tests_dir (str): Directory name which include tests.
        tests_path (str): Absolute path to the tests directory.
        fixtures_dir (str): Directory name which include tests datas.
        fixtures_path (str): Absolute path to the tests datas.
    """
    def __init__(self):
        # Base fixture datas directory
        self.application_path = os.path.abspath(
            os.path.dirname(video_registry.__file__)
        )
        self.package_path = os.path.normpath(
            os.path.join(
                os.path.abspath(
                    os.path.dirname(video_registry.__file__)
                ),
                "..",
            )
        )

        self.tests_dir = "tests"
        self.tests_path = os.path.join(
            self.package_path,
            self.tests_dir,
        )

        self.fixtures_dir = "data_fixtures"
        self.fixtures_path = os.path.join(
            self.tests_path,
            self.fixtures_dir
        )

    def format(self, content):
        """
        Format given string to include some values related to this application.

        Arguments:
            content (str): Content string to format with possible values.

        Returns:
            str: Given string formatted with possible values.
        """
        return content.format(
            HOMEDIR=os.path.expanduser("~"),
            PACKAGE=self.package_path,
            APPLICATION=self.application_path,
            TESTS=self.tests_path,
            FIXTURES=self.fixtures_path,
            VERSION=video_registry.__version__,
        )


@pytest.fixture(scope="session")
def temp_builds_dir(tmpdir_factory):
    """
    Shortand to prepare a temporary build directory where to create temporary
    content from tests.
    """
    fn = tmpdir_factory.mktemp("builds")
    return fn


@pytest.fixture(scope="module")
def test_settings():
    """
    Initialize and return settings for tests.

    Example:
        You may use it like: ::

            def test_foo(test_settings):
                print(test_settings.package_path)
                print(test_settings.format("foo: {VERSION}"))
    """
    return FixturesSettingsTestMixin()


@pytest.fixture
def db(caplog):
    """
    Initialize database, install models and release database under a single
    transaction.

    This is required to use database and models without to
    init them each time in your test functions. Once test is over, the database
    is flushed and closed so each test can start on a fresh new database.

    This fixture will return the current transaction cursor although you may not
    really need it.
    """
    caplog.set_level(logging.DEBUG)

    db = init_database()

    with db.transaction() as txn:  # `db` is my database object
        db.create_tables([Dummy, File])
        yield txn
        txn.rollback()

    db.close()


def get_settings():
    """
    Return default settings.
    """
    return Settings()


@pytest.fixture(scope="module")
def server_settings():
    """
    Function fixture for "get_settings"
    """
    return get_settings()


@pytest.fixture(scope="class")
def server_settings_class(request):
    """
    TestCase class fixture for "get_settings"
    """
    # set a class attribute on the invoking test context
    request.cls.server_settings = get_settings()


@pytest.fixture(scope="module")
def server_app(server_settings):
    """
    Return RegistryApplication instance.
    """
    return RegistryApplication(server_settings)
