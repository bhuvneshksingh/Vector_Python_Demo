from playhouse.shortcuts import model_to_dict

from db import SQLiteModel,myDB
import peewee as pw
import datetime
from Accounts import Accounts     
import logging


class Account(SQLiteModel):
    type = pw.CharField(null=True)
    title = pw.CharField(null=True)
    position = pw.CharField(null=True)
    
    class Meta:
        db_table = 'account'

def get_details():
    jsonRows =[]
    for row in Account.select():
        acc = Accounts(row.type, row.title, row.position)
        jsonRows.append(acc.__dict__)
    print('jsonRows',jsonRows)
    return jsonRows

def delete(account_type):
    Account.delete().where(Account.type == account_type).execute()

def create_activity(data):
    Account.create(type = data["type"],
                                 title = data["title"],
                                   position = data["position"])

def create_activities(data):
    if Account.select().__len__()==0:
        with myDB.atomic():
            query= Account.insert_many(data)
            query.execute()

