from flask import Flask, jsonify, request
from peeweee import *

db = PostgresqlDatabase()

classBaseModel(Model):
  class Meta:
    database = db

db.connect()
db.drop_tables()
db.create_tables()

