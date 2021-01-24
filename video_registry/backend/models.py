import datetime

from peewee import SqliteDatabase, Model, DateTimeField, CharField, ForeignKeyField, IntegerField


# Lazy database connector
VideoRegistryDatabase = SqliteDatabase(None)


class BaseModel(Model):
    """
    Base model to share the same database connector
    """
    class Meta:
        database = VideoRegistryDatabase


class File(BaseModel):
    """
    Video file
    """
    created = DateTimeField(index=True, null=False)
    path = CharField(max_length=255, null=False)
    size = IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.created = datetime.datetime.now()
        return super().save(*args, **kwargs)


def create_tables():
    with VideoRegistryDatabase:
        VideoRegistryDatabase.create_tables([File])
