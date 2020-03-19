import os
import sqlite3
from sqlite3 import Error


PATH = ''


class Database:
    def __init__(self):
        pass

    def connect(self):
        conn = None
        try:
            if os.path.exists(PATH):
                conn = sqlite3.connect(PATH)
                # print('Connectd to db:', db, '  Successfully!')
            else:
                print("Could not connect to Database: NOT FOUND!")
        except Error as e:
            print(e)

        return conn


if __name__ == '__main__':
    pass
