import sqlite3

from Python.generateContentFilteringLatentMatrix import  generateContentFilteringLatentMatrix
from Python.generateMovieDB import generateMovieDB
from app import db

def initialzeLatentMatrix():
    generateContentFilteringLatentMatrix()

def initializeDB():
    conn = sqlite3.connect("database.db")
    db.create_all()
    conn.close()

def initializeMovieDB():
    generateMovieDB()

if __name__ == "__main__":
    initialzeLatentMatrix()
    initializeDB()
    initializeMovieDB()