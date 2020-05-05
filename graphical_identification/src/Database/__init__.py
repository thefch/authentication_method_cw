import json
import os
import sqlite3
from sqlite3 import Error

from src.Account import Account
from src.Image import Image
from src.Key import Key

PATH = 'database/db.sqlite3'


class Database:
    def __init__(self):
        pass

    @staticmethod
    def connect():
        conn = None
        try:
            if os.path.exists(PATH):
                conn = sqlite3.connect(PATH, detect_types=sqlite3.PARSE_DECLTYPES)
                # print('Connected to db:', PATH, '  Successfully!')
            else:
                print("Could not connect to Database: NOT FOUND!")
        except Error as e:
            raise e
            # print(e)

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
                clicks = json.loads(acc[6])
                keydowns = json.loads(acc[5])
                comb = json.loads(acc[4])

                keyword_info = {
                    'grid_keyword': clicks,
                    'keydown_keyword': keydowns,
                    'entered_keys': comb,
                    'final_keyword': dic}
                account = Account(acc[1], keyword_info, acc[0])
                if acc[7]:
                    account.keydown_is_inorder(acc[7])
                print("Account retrieved -> %s" % account)

                img = self.get_image_entry(account)
                account.set_image(img)
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
        final_keyword = json.dumps(account.get_formatted_combination())
        # entered_keyword = account.get_keyword_info('entered_keyword')
        entered_keys = json.dumps(account.get_keyword_info('entered_keys'))
        # keydown_keyword = account.get_keyword_info('keydown_keyword')
        keydown_keyword = json.dumps(account.get_keyword_info('keydown_keyword'))
        # grid_keyword = account.get_keyword_info('grid_keyword')
        grid_keyword = json.dumps(account.get_keyword_info('grid_keyword'))

        keydown_inorder = account.get_keydown_in_order()
        email = account.get_email()
        query = """INSERT INTO accounts_tb ('username','keyword','email','entered_keys','keydown_keyword','grid_keyword','keydown_inorder')
                    VALUES(?,?,?,?,?,?,?);"""

        args = (username, final_keyword, email, entered_keys, keydown_keyword, grid_keyword,keydown_inorder)

        updated_acc = account
        successful = False
        try:
            cur.execute(query, args)
            con.commit()
            # print("Account added to db: ", account)
            temp_id = self.get_account_id(account.get_username())

            updated_acc.set_id(temp_id)
            successful = True
            print('Account created: ', updated_acc)
        except Exception as err:
            raise err
            # print(err)

        cur.close()
        con.close()
        return successful, updated_acc

    def set_account_img_id(self, account, img_id) -> bool:
        con = self.connect()
        cur = con.cursor()
        successful = False

        query = """UPDATE accounts_tb
                      SET image_id=? 
                      WHERE id=?"""
        args = (img_id, account.get_id())

        try:
            cur = con.cursor()
            cur.execute(query, args)
            con.commit()
            successful = True
            print(' Image id updated for user:', account.get_username(), '  successful:', successful)
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
                        'entered_keys': acc[4],
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
            raise err
            # print(err)

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

    def get_image_entry(self, acc: Account, name_: str = None) -> Image:

        name = ''
        if name_ is not None:
            name = name_
        else:
            name = acc.get_username()

        query = """SELECT * from images_tb where name = ? and account_id=?"""
        args = (name, acc.get_id())

        con = self.connect()
        cur = con.cursor()

        img = None
        try:
            cur.execute(query, args)
            entry = cur.fetchone()
            if entry is not None:
                photo_path = os.path.abspath("static/images/users/") + '\\' + str(name) + ".jpg"
                # photoPath = "images/" + str(name) + ".jpg"
                self.__write_to_file(entry[1], photo_path)
                print("Image stored on disk :", photo_path)

                img = Image(photo_path, name, entry[0], acc.get_id())
        except Exception as error:
            raise error

        cur.close()
        con.close()

        return img

    @staticmethod
    def __convert_to_binary_data(filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData

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
    def __write_to_file(data, filepath):
        # Convert binary data to proper format and write it on Hard Disk
        try:
            with open(filepath, 'wb') as file:
                file.write(data)
            print("Stored blob data into: ", filepath, "\n")
        except Exception as e:
            raise e


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
