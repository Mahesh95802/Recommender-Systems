from genericpath import isdir
import sqlite3

from python.GenerateLatentMatrices import  generateLatentMatrices
from python.GenerateMovieDB import generateMovieDB
from app import db
import os

def createDirectories():
    if(not(os.path.isdir("/dataset"))):
        os.mkdir("/dataset")
    if(not(os.path.isdir("/data"))):
        os.mkdir("/data")
    

def initialzeLatentMatrix():
    generateLatentMatrices()

def initializeDB():
    conn = sqlite3.connect("data/database.db")
    db.create_all()
    conn.close()

def initializeMovieDB():
    generateMovieDB()

if __name__ == "__main__":
    # createDirectories()
    initialzeLatentMatrix()
    initializeDB()
    initializeMovieDB()