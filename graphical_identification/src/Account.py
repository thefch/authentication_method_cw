from src.Image import Image
from src.Key import Key

# TODO:
#     first create an account with username and combination
#     save the image with that user;s id
class Account:
    def __init__(self, username_: str, keyword_info_: [str], id_: int = None):
    # def __init__(self, username_: str, keyword_info_: [str], image_id_: int, email_: str = None, id_: int = None):
        self.__username = username_
        self.__final_combination = keyword_info_['final_combination']
        self.__entered_keyword   = keyword_info_['entered_keyword']
        self.__keydown_keyword   = keyword_info_['keydown_keyword']
        self.__grid_keydown = keyword_info_['grid_keyword']
        self.__keyword_info = keyword_info_
        # self.__email = email_
        self.__image_id = None
        self.__id = id_ if id_ is not None else -1

    def get_username(self):
        return self.__username

    def get_keyword_info(self,name=None):
        if name is None:
            return self.__keyword_info
        else:
            return self.__keyword_info[name]
    # def get_email(self):
    #     return self.__email

    def get_image_id(self):
        return self.__image_id

    def get_id(self):
        return self.__id

    # def get_image_file(self):
    #     return self.__image

    # def set_image_file(self, img_: Image):
    #     self.__image = img_

    def set_id(self, id_: int):
        self.__id = id_

    # def set_combination(self, combination_: [Key]):
    #     self.__combination = combination_

    def __str__(self):
        return "%s username:%s pass:%s img_id:%s" % (
            self.__id, self.__username, self.__final_combination, self.__image_id)


if __name__ == '__main__':
    pass
