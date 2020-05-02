import codecs
import json
import os
import pickle
import sqlite3
from sqlite3 import Error

from src.Account import Account
from src.Image import Image
from src.Key import Key

PATH = 'database/db.sqlite3'

# protocol = 0
# sqlite3.register_converter("pickle", pickle.loads)
#
# sqlite3.register_adapter(list, pickle.dumps)
# sqlite3.register_adapter(set, pickle.dumps)


class Database:
    def __init__(self):
        # self.connection = self.connect()
        pass

    # def __delete__(self):
    #     cur = self.connection.cursor()
    #     cur.close()
    #     self.connection.close()
    #     print("Database disconnected!")

    @staticmethod
    def connect():
        conn = None
        try:
            if os.path.exists(PATH):
                conn = sqlite3.connect(PATH,detect_types=sqlite3.PARSE_DECLTYPES)
                # print('Connected to db:', PATH, '  Successfully!')
            else:
                print("Could not connect to Database: NOT FOUND!")
        except Error as e:
            print(e)

        return conn

    # checks if an account already exists in the database
    def account_exists(self, username: str) -> bool:
        con = self.connect()
        cur = con.cursor()

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

        cur.close()
        con.close()
        return exists

    def account_exists_by_id(self, user_id: int) -> bool:
        con = self.connect()
        cur = con.cursor()

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

        cur.close()
        con.close()
        return exists

    # returns an Account object
    def get_account(self, username: str, user_id=-1) -> Account:
        con = self.connect()
        cur = con.cursor()

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
                dic = self.__get_enum_combination_format(acc[2])
                keyword_info = {
                    'grid_keyword': acc[6],
                    'keydown_keyword': acc[5],
                    'entered_keyword': acc[4],
                    'final_keyword': dic}
                account = Account(acc[1], keyword_info, acc[0])

                print("Account retrieved -> %s" % account.get_username())
        except Error as err:
            raise err

        cur.close()
        con.close()
        return account

    # returns an Accounts id
    def get_account_id(self, username: str) -> int:
        con = self.connect()
        cur = con.cursor()

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

        cur.close()
        con.close()
        return user_id

    # add an account entry in the account table
    def add_account(self, account: Account) -> [bool, Account]:
        con = self.connect()
        cur = con.cursor()

        username = account.get_username()

        final_keyword = account.get_keyword_info('final_keyword')
        # final_keyword = json.dumps(final_kwrd, cls=EnumEncoder).encode('utf-8')

        final_keyword = json.dumps(account.get_formatted_combination())
        print("The type after conversion to bytes is : " + str(type(final_keyword)))
        print("The value after conversion to bytes is : " + str(final_keyword))

        entered_keyword = account.get_keyword_info('entered_keyword')
        keydown_keyword = account.get_keyword_info('keydown_keyword')
        grid_keyword = account.get_keyword_info('grid_keyword')
        email = account.get_email()
        query = """INSERT INTO accounts_tb ('username','keyword','email','entered_keyword','keydown_keyword','grid_keyword')
                    VALUES(?,?,?,?,?,?);"""

        args = (username, final_keyword, email, entered_keyword, keydown_keyword, grid_keyword)

        updated_acc = account
        successful = False
        try:
            cur.execute(query, args)
            con.commit()
            # print("Account added to db: ", account)
            temp_id = self.get_account_id(account.get_username())

            updated_acc.set_id(temp_id)
            successful = True
            print('Account created: ', temp_id, account.get_username())
        except Exception as err:
            print(err)

        cur.close()
        con.close()
        return successful, updated_acc

    def set_account_img_id(self, acc, img_id) -> bool:
        con = self.connect()
        cur = con.cursor()
        successful = False

        query = """UPDATE accounts_tb
                      SET image_id=? 
                      WHERE id=?"""
        args = (img_id, acc.get_id())

        try:
            cur = con.cursor()
            cur.execute(query, args)
            con.commit()
            successful = True
            print(' Image id updated for user:', acc.get_username())
        except Exception as e:
            raise e
        cur.close()
        con.close()
        return successful

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

        cursor.close()
        conn.close()
        return successful

    # delete all the entries(users) from the account table
    def delete_all_users(self) -> bool:
        con = self.connect()
        cur = con.cursor()

        successful = False
        try:
            user_ids = self.get_all_accounts_ids()

            for i in user_ids:
                query = "DELETE from accounts_tb where id=?"
                args = (i,)

                cur.execute(query, args)
                con.commit()

                self.delete_account(i)

                # print("Accound deleted: " + str(id))

            successful = True
        except Error as err:
            print(err)

        cur.close()
        con.close()
        return successful

    # return all accounts in the database
    def get_all_accounts(self) -> [Account]:
        con = self.connect()
        cur = con.cursor()

        query = "SELECT * FROM accounts_tb"
        accounts = []
        try:
            cur.execute(query)
            temp_accounts = cur.fetchall()
            if temp_accounts is not None:
                for acc in temp_accounts:
                    keyword_info = {
                        'grid_keyword': acc[6],
                        'keydown_keyword': acc[5],
                        'entered_keyword': acc[4],
                        'final_keyword': acc[2]}
                    account = Account(acc[1], keyword_info, acc[0])
                    accounts.append(account)

        except Error as err:
            print(err)

        cur.close()
        con.close()
        return accounts

    def get_all_accounts_ids(self) -> [Account]:
        con = self.connect()
        cur = con.cursor()

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

        cur.close()
        con.close()
        return ids

    def add_image_entry(self, image_, acc, name_=None) -> [bool, Image]:
        con = self.connect()
        cur = con.cursor()

        file = self.__convert_to_binary_data(image_)
        # type(image_)
        query = """INSERT INTO images_tb ('image','name','account_id')
                        VALUES(?,?,?);"""

        name = ''
        if name_ is not None:
            name = name_
        else:
            name = acc.get_username()

        args = (file, name, acc.get_id())
        successful = False
        img = None
        try:
            cur.execute(query, args)

            con.commit()

            successful = True
            print('Image entry added: ', image_)

            im_id = self.get_image_id(name, acc.get_id())
            self.set_account_img_id(acc, im_id)
            img = Image(image_, name)

            successful = True
        except Exception as err:
            print(err)

        cur.close()
        con.close()

        return successful, img

    def get_image_id(self, img_name, account_id) -> int:
        con = self.connect()
        cur = con.cursor()
        im_id = None

        query = "SELECT * FROM images_tb WHERE name=? AND account_id=?"
        args = (img_name, account_id,)

        try:
            cur.execute(query, args)
            entry = cur.fetchone()
            if entry is not None:
                im_id = entry[0]
                print("Image ID with name ", img_name, " -> ", img_name)
        except Error as err:
            raise err

        cur.close()
        con.close()
        return im_id

    def get_image_entry(self, acc: Account, name_: str = None):
        con = self.connect()
        cur = con.cursor()

        query = """SELECT * from images_tb where name = ? and account_id=?"""

        if name_ is not None:
            name = name_
        else:
            name = acc.get_username()

        args = (name, name, acc.get_id())
        try:

            cur.execute(query, args)
            entry = cur.fetchone()
            print(entry[1])
            photo_path = os.path.abspath("../../static/images/") + '\\' + str(name) + ".jpg"
            # photoPath = "images/" + str(name) + ".jpg"
            self.__write_to_file(entry[1], photo_path)
            print("Image stored on disk :", photo_path)
        except Exception as error:
            print(error)

        cur.close()
        con.close()

    @staticmethod
    def __convert_to_binary_data(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

    @staticmethod
    def __convert_from_pickle(file):
        # Convert form pickle obj to python
        # res_dict = json.loads(file.decode('utf-8'))
        #
        # # printing type and dict
        # print("The type after conversion to dict is : " + str(type(res_dict)))
        # print("The value after conversion to dict is : " + str(res_dict))
        # D2 = eval(file)
        print('type:',type(file))
        print(file)
        x = pickle.loads(file.decode('base64', 'strict'))
        print(x)
        return 1

    @staticmethod
    def __get_enum_combination_format(input_file):
        inp = json.loads(input_file)

        out = []
        for entry in inp:
            pair = []
            # print(entry)

            for i in entry:
                # print(i,end=' ')
                if i in Key.get_names():
                    k = Key.get_val(i)
                    pair.append(k)
                else:
                    pair.append(i)
            out.append(pair)
        return out

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
    database = Database()

    acc = database.get_account('123')
    print(acc)
    # x=[['KEYDOWN', 'q'], ['KEYDOWN', 'q'], ['KEYDOWN', 'q'], ['CLICK', 1], ['CLICK', 2], ['CLICK', 3], ['CLICK', 4]]
    # x = json.dumps(x)
    # print(database.get_enum_combination_format(x))
    #
    # img = Image(img_path)
    # acc = Account('test','KEYWQORd')
    # empPhoto = convertToBinaryData(img_path)
    # database.add_image_entry(empPhoto, 1)

    # database.get_image_entry(1)
    # database.get_image_entry(1)
