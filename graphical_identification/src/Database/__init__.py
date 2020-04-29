import os
import sqlite3
from sqlite3 import Error

from src.Account import Account
from src.Image import Image

PATH = 'database/db.sqlite3'


class Database:

    def __init__(self):
        self.connection = self.connect()

    def __delete__(self):
        cur = self.connection.cursor()
        cur.close()
        self.connection.close()
        print("Database disconnected!")

    @staticmethod
    def connect():
        conn = None
        try:
            if os.path.exists(PATH):
                conn = sqlite3.connect(PATH)
                print('Connected to db:', PATH, '  Successfully!')
            else:
                print("Could not connect to Database: NOT FOUND!")
        except Error as e:
            print(e)

        return conn

    # checks if an account already exists in the database
    def account_exists(self, username: str) -> bool:
        cur = self.connection.cursor()
        query = "SELECT * FROM accounts_tb WHERE username=?"
        args = (username,)

        exists = False
        try:
            cur.execute(query, args)
            acc = cur.fetchone()

            if acc is not None:
                exists = True
        except Error as err:
            raise err

        return exists

    def account_exists_by_id(self, user_id: int) -> bool:
        cur = self.connection.cursor()
        query = "SELECT * FROM accounts_tb WHERE id=?"
        args = (user_id,)

        exists = False
        try:
            cur.execute(query, args)
            acc = cur.fetchone()

            if acc is not None:
                exists = True
        except Error as err:
            raise err

        return exists

    # returns an Account object
    def get_account(self, username: str, user_id=-1) -> Account:

        cur = self.connection.cursor()

        if user_id != -1:
            query = """SELECT * FROM accounts_tb WHERE id=?"""
            args = (user_id,)
        else:
            query = """SELECT * FROM accounts_tb WHERE username=?"""
            args = (username,)

        account = None
        try:
            cur.execute(query, args)
            acc = cur.fetchone()
            if acc is not None:
                keyword_info={
                    'grid_keyword':acc[6],
                    'keydown_keyword':acc[5],
                    'entered_keyword':acc[4],
                    'final_combination':acc[2]}
                account = Account(acc[1], keyword_info,acc[0])

                print("Account retrieved -> %s" % account.get_username())
        except Error as err:
            raise err

        return account

    # returns an Accounts id
    def get_account_id(self, username: str) -> int:

        cur = self.connection.cursor()

        query = "SELECT * FROM accounts_tb WHERE username=?"
        args = (username,)
        user_id = None
        try:
            cur.execute(query, args)
            account = cur.fetchone()
            if account is not None:
                # print(account)
                user_id = account[0]
                print("User ID with username", username, " -> ", user_id)
                # print(user_id)
        except Error as err:
            raise err
        return user_id

    # add an account entry in the account table
    def add_account(self, account: Account) -> [bool, Account]:
        cur = self.connection.cursor()
        username        = account.get_username()
        final_keyword   = account.get_keyword_info('final_keyword')
        entered_keyword = account.get_keyword_info('entered_keyword')
        keydown_keyword = account.get_keyword_info('keydown_keyword')
        grid_keyword    = account.get_keyword_info('grid_keyword')

        query = """INSERT INTO accounts_tb ('username','keyword','email','entered_keyword','keydown_keyword','grid_keyword')
                    VALUES(?,?,?,?,?,?);"""

        args = (username, username,final_keyword,entered_keyword,keydown_keyword,grid_keyword)

        updated_acc = account
        successful = False
        try:
            cur.execute(query, args)
            self.connection.commit()
            # print("Account added to db: ", account)
            temp_id = self.get_account_id(account.get_username())

            updated_acc.set_id(temp_id)
            successful = True
        except Exception as err:
            print(err)

        return successful, updated_acc

    # delete an account by it's ID
    def delete_account(self, user_id: int):
        exists = self.account_exists_by_id(user_id)
        successful = False
        if not exists:
            return successful

        successful = self.__delete_user(user_id)
        print('Delete user:', successful)

        return successful

    # delete an entry from the Account table
    # is called from delete account
    def __delete_user(self, user_id: int) -> bool:
        conn = self.connect()
        cursor = conn.cursor()
        query = "DELETE FROM accounts_tb WHERE id=?"
        args = (user_id,)
        successful = False
        try:
            cursor.execute(query, args)
            conn.commit()
            print("Deleted from db: " + str(user_id))

            successful = True
        except Error as err:
            print(err)

        return successful

    # delete all the entries(users) from the account table
    def delete_all_users(self) -> bool:
        cur = self.connection.cursor()
        successful = False
        try:
            user_ids = self.get_all_accounts_ids()

            for i in user_ids:
                query = "DELETE from accounts_tb where id=?"
                args = (i,)

                cur.execute(query, args)
                self.connection.commit()

                self.delete_account(i)

                # print("Accound deleted: " + str(id))

            successful = True
        except Error as err:
            print(err)

        return successful

    # return all accounts in the database
    def get_all_accounts(self) -> [Account]:
        cur = self.connection.cursor()
        query = "SELECT * FROM accounts_tb"
        accounts = []
        try:
            cur.execute(query)
            temp_accounts = cur.fetchall()
            if temp_accounts is not None:
                for acc in temp_accounts:
                    keyword_info={
                        'grid_keyword':acc[6],
                        'keydown_keyword':acc[5],
                        'entered_keyword':acc[4],
                        'final_combination':acc[2]}
                    account = Account(acc[1], keyword_info,acc[0])
                    accounts.append(account)

        except Error as err:
            print(err)

        return accounts

    def get_all_accounts_ids(self) -> [Account]:
        cur = self.connection.cursor()
        query = "SELECT * FROM accounts_tb"
        ids = []
        try:
            cur.execute(query)
            temp_accounts = cur.fetchall()
            if temp_accounts is not None:
                for a in temp_accounts:
                    ids.append(a[0])

        except Error as err:
            print(err)

        return ids

    def add_image_entry(self, image_, acc: Account, name_: str = None):
        type(image_)
        query = """INSERT INTO images_tb ('image','name','account_id')
                        VALUES(?,?,?);"""

        if not None:
            name = name_
        else:
            name = acc.get_username()

        args = (image_, name, acc.get_id())
        successful = False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, args)

            self.connection.commit()

            successful = True
        except Exception as err:
            print(err)

        return successful

    def get_image_entry(self, acc: Account, name_: str = None):
        query = """SELECT * from images_tb where name = ? and account_id=?"""

        if name_ is not None:
            name = name_
        else:
            name = acc.get_username()

        args = (name, name, acc.get_id())
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, args)
            entry = cursor.fetchone()
            print(entry[1])
            photo_path = os.path.abspath("../../static/images/") + '\\' + str(name) + ".jpg"
            # photoPath = "images/" + str(name) + ".jpg"
            self.__write_to_file(entry[1], photo_path)
            print("Image stored on disk :", photo_path)
        except Exception as error:
            print(error)

    @staticmethod
    def __convert_to_binary_data(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    @staticmethod
    def __write_to_file(data, filename):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")


if __name__ == '__main__':
    testing = True
    PATH = '../../database/db.sqlite3'
    img_path = "../../static/images/kitten.jpg"
    # database = Database()
    # img = Image(img_path)
    # acc = Account('test','KEYWQORd')
    # empPhoto = convertToBinaryData(img_path)
    # database.add_image_entry(empPhoto, 1)

    # database.get_image_entry(1)
    # database.get_image_entry(1)
