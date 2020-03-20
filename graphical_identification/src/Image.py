class Image:

    def __init__(self, img_path_, name_, id_=None):
        self.__img_path = img_path_
        self.__name = name_

        self.__id = id_ if id_ is not None else -1
        self.__account_id = -1
        self.__init_image()

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

    def __init_image(self):
        pass

    def __str__(self):
        return 'Image: %s %s account_id:%s  path:%s ' % (self.__id, self.__name, self.__account_id, self.__img_path)


if __name__ == '__main__':
    pass
