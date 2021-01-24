import logging

import pytest

from peewee import OperationalError as PeeWeeOperationalError

from video_registry.backend.models import File


def test_db_01_fixture(caplog, db):
    """
    Ensure 'db' fixture is working well, meaning it open and initialize database,
    install models all this in a single transaction, then once test is over, the
    database is flushed and closed.
    """
    caplog.set_level(logging.DEBUG)

    # Create a basic object
    obj = File.create(
        path="Charlie",
    )

    # Check object has been correctly saved and not more
    assert File.select().count() == 1
    assert File.get_by_id(obj.id).path == "Charlie"


def test_db_02_fixture(caplog):
    """
    A test which should follow 'test_db_01_fixture' to ensure each new test can
    use a new database.

    Here, trying to use Model should fail with an exception since database
    have not been initialized.
    """
    caplog.set_level(logging.DEBUG)

    with pytest.raises(PeeWeeOperationalError):
        File.select().count()
