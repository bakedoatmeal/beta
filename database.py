from dns.query import tls
from flask_pymongo import PyMongo
from flask import Flask, render_template
from pymongo import MongoClient
from flask import Flask, render_template, request, redirect, url_for
from  bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import pymongo
import certifi

app = Flask(__name__)
ca = certifi.where()
load_dotenv()
DATABASE_URL = f'mongodb+srv://janecui:{os.environ.get("password")}@playlistr.k3tyy.mongodb.net/Playlister?retryWrites=true&w=majority'
client = MongoClient(DATABASE_URL, tlsCAFile=ca)
app.config['MONGO_URI'] = DATABASE_URL
mongo = PyMongo(app, tlsCAFile=ca)
db = client.Donations
climbers = db.climbers
climbs = db.climbs
gyms = db.gyms
