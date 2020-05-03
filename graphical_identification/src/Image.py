import os


class Image:

    def __init__(self, img_path_, name_, id_=None, acc_id_=None):
        self.__img_path = img_path_
        self.__name = name_
        self.__id = id_ if id_ is not None else -1
        self.__account_id = acc_id_ if acc_id_ is not None else -1

    def get_path(self):

        return self.__img_path

    def get_account_id(self):
        return self.__account_id

    def get_name(self):
        return self.__name

    def get_id(self):
        return self.__id

    def set_account_id(self, id_: int):
        self.__account_id = id_

    def read(self):
        try:
            img = open(self.__img_path, 'r')
        except Exception as e:
            img = None
            raise e

        return img

    def get_local_path(self,upload_dir_path:str)->str:
        image_path = self.__img_path.replace("\\","/").split(upload_dir_path)[1]
        image_path = upload_dir_path + image_path
        return image_path

    def __str__(self):
        return '\t Image: %s id:%d account_id:%s  name:%s' % (
            self.__img_path, self.__id, self.__account_id, self.__name)


if __name__ == '__main__':
    pass
