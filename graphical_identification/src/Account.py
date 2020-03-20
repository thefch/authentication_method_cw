from src.Image import Image
from src.Key import Key


class Account:

    def __init__(self, username_: str, password_: str, image_id_: int, email_: str = None, id_: int = None):
        self.__username = username_
        self.__password = password_
        self.__email = email_
        self.__image_id = image_id_
        self.__id = id_ if id_ is not None else -1
        self.__image = None
        self.__combination = None

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email

    def get_image_id(self):
        return self.__image_id

    def get_id(self):
        return self.__id

    def get_image_file(self):
        return self.__image

    def set_image_file(self, img_: Image):
        self.__image = img_

    def set_id(self, id_: int):
        self.__id = id_

    def set_combination(self, combination_: [Key]):
        self.__combination = combination_

    def __str__(self):
        return "%s username:%s pass:%s email:%s im_id:%s" % (
            self.__id, self.__username, self.__password, self.__email, self.__image_id)


if __name__ == '__main__':
    pass
