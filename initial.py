from genericpath import isdir
import sqlite3
from app import db, app
import os

from python.GenerateLatentMatrices import  generateLatentMatrices
from python.GenerateMovieDB import generateMovieDB

def createDirectories():
    if(not(os.path.isdir("/dataset"))):
        os.mkdir("/dataset")
    if(not(os.path.isdir("/data"))):
        os.mkdir("/data")
    

def initialzeLatentMatrix():
    generateLatentMatrices()

def initializeDB():
    conn = sqlite3.connect("data/database.db")
    with app.app_context():
        db.create_all()
    conn.close()

def initializeMovieDB():
    generateMovieDB()

if __name__ == "__main__":
    createDirectories()
    initialzeLatentMatrix()
    initializeDB()
    initializeMovieDB()