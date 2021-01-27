import datetime

from peewee import (
    SqliteDatabase, Model, DateTimeField, CharField, ForeignKeyField,
    IntegerField
)


# Lazy database connector
VideoRegistryDatabase = SqliteDatabase(None)


class BaseModel(Model):
    """
    Base model to share the same database connector
    """
    class Meta:
        database = VideoRegistryDatabase


class Dummy(BaseModel):
    """
    A simple dummy object for testing purpose only
    """
    created = DateTimeField(index=True, null=False)
    name = CharField(max_length=25, null=False)

    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        return super().save(*args, **kwargs)


class File(BaseModel):
    """
    Video file
    """
    created = DateTimeField(index=True, null=False)
    absolute_path = CharField(max_length=255, null=False)
    relative_path = CharField(max_length=255, null=False)
    basedir = CharField(max_length=255, null=False)
    extension = CharField(max_length=25, null=False)
    size = IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        return super().save(*args, **kwargs)


def create_tables():
    with VideoRegistryDatabase:
        VideoRegistryDatabase.create_tables([Dummy, File])
