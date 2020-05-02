import json

from src.Image import Image
from src.Key import Key


# TODO:
#     first create an account with username and combination
#     save the image with that user;s id
class Account:
    def __init__(self, username_: str, keyword_info_: [str], id_: int = None):
        # def __init__(self, username_: str, keyword_info_: [str], image_id_: int, email_: str = None, id_: int = None):
        self.__username = username_
        self.__final_keyword = keyword_info_['final_keyword']
        self.__entered_keyword = keyword_info_['entered_keyword']
        self.__keydown_keyword = keyword_info_['keydown_keyword']
        self.__grid_keydown = keyword_info_['grid_keyword']
        self.__keyword_info = keyword_info_
        self.__email = ''
        self.__image_id = None
        self.__id = id_ if id_ is not None else -1

    def get_username(self):
        return self.__username

    def get_keyword_info(self, name=None):
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

    def set_id(self, id_: int):
        self.__id = id_

    def get_formatted_combination(self):
        out = []
        for entry in self.__final_keyword:
            pair = []
            for k in entry:
                if type(k) == Key:
                    pair.append(k.name)
                else:
                    pair.append(k)
            out.append(pair)
        return out



    def __str__(self):
        return "%s username:%s pass:%s img_id:%s" % (
            self.__id, self.__username, self.__final_keyword, self.__image_id)

    def get_email(self):
        return self.__email


if __name__ == '__main__':
    comb = [(Key.KEYDOWN, 'd'), (Key.KEYDOWN, 'd'), (Key.KEYDOWN, 'd'), (Key.CLICK, 1), (Key.CLICK, 3), (Key.CLICK, 6),
            (Key.CLICK, 13)]

    keyword_info = {
        'grid_keyword': '',
        'keydown_keyword': '',
        'entered_keyword': '',
        'final_keyword': comb
    }
    acc = Account('123', keyword_info)
    acc.get_combination_dict_to_str()
