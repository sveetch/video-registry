"""
Initialize database for peewee connector
"""
from .models import VideoRegistryDatabase


def init_database():
    """
    Initialize the database with correct db settings
    """
    VideoRegistryDatabase.init(":memory:")

    return VideoRegistryDatabase
