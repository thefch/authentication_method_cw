import os

from src.Account import Account
from src.Key import Key
from PIL import Image as Image


def get_default_images(DEFAULT_IMAGES_PATH) -> [str]:
    images = os.listdir(DEFAULT_IMAGES_PATH)
    return [DEFAULT_IMAGES_PATH + x for x in images]


def filter_data(combination: [str], keys: [str], clicks: [str]):
    new_combination = []
    new_keys = []
    new_clicks = []

    combination = combination.split('/')
    new_combination = [c for c in combination if c.strip() is not '']

    keys = keys.split('/')
    new_keys = [k for k in keys if k.strip() is not '']

    clicks = clicks.split('/')
    new_clicks = [int(c) for c in clicks if c.strip() is not '']

    return new_combination, new_keys, new_clicks


def validate_keyword(entered_keyword: str, keydown_keyword: str, grid_keyword: str) -> [bool, str, str, str]:
    start_full = entered_keyword.find(':') + 1
    start_keys = keydown_keyword.find(':') + 1
    start_clicks = grid_keyword.find(':') + 1

    successful = False
    keys = []
    combination = []
    clicks = []

    if start_clicks is -1 or start_keys is -1 or start_full is -1:
        # ERROR
        successful = False
    else:
        keys = keydown_keyword[start_keys:]
        combination = entered_keyword[start_full:]
        clicks = grid_keyword[start_clicks:]

        combination, keys, clicks = filter_data(combination, keys, clicks)
        print('keys:', keys)
        print('clicks', clicks)
        print('combination:', combination)
        successful = True

    return successful, combination, keys, clicks


def set_combination(combination: [str], keys: [str], clicks: [int]):
    final_combination = []
    key_counter = 0
    click_counter = 0

    for entry in combination:
        pair = None

        if entry is 'C':
            pair = (Key.CLICK, clicks[click_counter])
            click_counter += 1
        elif entry is 'K':
            pair = (Key.KEYDOWN, keys[key_counter])
            key_counter += 1

        if pair is not None:
            final_combination.append(pair)
        else:
            raise None

    print('FINAL:', final_combination)

    return final_combination


def check_image_size(path: str, name: str) -> bool:
    checked = False
    try:
        # img = Image.open(dir_path+name)
        with open(path + name, 'r+b') as f:
            with Image.open(f) as img:

                if img is not None:
                    img_width, img_height = img.size
                    print(name, ' -> width:', img_width, ' height:', img_height)

                    out_img = None

                    if not (img_height == 790 and img_width == 770):
                        # if (img_width > 800 or img_height > 800) or (img_height < 700 or img_height < 700):
                        print('editing image:', name)
                        out_img = img.resize([790, 770])
                        # out_img = resizeimage.resize_cover(img, [790, 770])
                        img_width, img_height = out_img.size
                        print(' ---> width:', img_width, ' height:', img_height)

                        out_img.save(path + name, img.format)
                        checked = True
                    # elif img_height < 700 or img_height < 700:
                    #     print('editing image:', name)
                    #     out_img = resizeimage.resize_cover(img, [790, 770])
                    #     img_width, img_height = out_img.size
                    #     print(' ---> width:', img_width, ' height:', img_height)
                    #
                    #     out_img.save(path + name, img.format)
                    #     checked = True
    except:
        pass

    return checked


def check_default_images(images_paths: [str], dir_path):
    for name in images_paths:
        # img = None
        checked = check_image_size(dir_path, name)
        if not checked:
            print('!!! Error resizing -> ', name)


def create_account(username: str, keyword: str, image_path: str):
    acc = Account(username, keyword, )
    #   TODO:
    #       implement account population
    # get image first and save it

    #
    pass


if __name__ == '__main__':
    default_images_path = 'static/images/default/'
    DEFAULT_IMAGES = os.listdir(default_images_path)
    check_default_images(DEFAULT_IMAGES, default_images_path)
