import peewee as pw
import time
import logging

myDB = pw.SqliteDatabase('VectorDemo.db')


class SQLiteModel(pw.Model):
    
    class Meta:

        database = myDB
        primary_key = False

class SQLiteModelTs(SQLiteModel):

    updated_at = pw.IntegerField(null=True)

    def save(self, *args, **kwargs):
        self.updated_at = long(time.time())
        return super(SQLiteModel, self).save(*args, **kwargs)

    @classmethod
    def update(cls, *args, **update):
        update['updated_at'] = long(time.time())
        return super(SQLiteModelTs, cls).update(*args, **update)


def connect_db():
    myDB.connect()
    logging.info('connected to db')


def close_db():
    myDB.close()
    logging.info('db connection closed')
