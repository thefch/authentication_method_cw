import os

from src.Account import Account
from src.Database import Database
from src.Key import Key
from PIL import Image as Image

MAX_POINTS = 4
database = Database()


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
    # the index of the text value from the grid page
    start_full = entered_keyword.find(':') + 1
    start_keys = keydown_keyword.find(':') + 1
    start_clicks = grid_keyword.find(':') + 1

    is_valid = False
    keys = []
    combination = []
    clicks = []

    if start_clicks is -1 or start_keys is -1 or start_full is -1:
        # ERROR
        is_valid = False
    else:
        keys = keydown_keyword[start_keys:]
        combination = entered_keyword[start_full:]
        clicks = grid_keyword[start_clicks:]
        print('grid kwrd:', len(clicks), '  entered:', len(combination))
        combination, keys, clicks = filter_data(combination, keys, clicks)

        if len(combination) == 0 or len(clicks) == 0 or len(clicks) < MAX_POINTS:
            is_valid = False
        else:
            print('keys:', keys)
            print('clicks', clicks)
            print('combination:', combination)
            is_valid = True

    return is_valid, combination, keys, clicks


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


def create_account(username: str, keyword_info: [str], image_path: str) -> bool:
    acc = Account(username, keyword_info)

    acc_added, acc = database.add_account(acc)

    img_added, img = database.add_image_entry(image_path, acc, acc.get_username())

    if acc_added and img_added:
        return True

    #   TODO:
    #       implement account population

    return False


def get_account(username):
    acc = database.get_account(username)
    return acc


def check_if_credential_match(username: str, keyword_info: {}) -> bool:

    account = database.get_account(username)

    return account.match(keyword_info)

    # return False


if __name__ == '__main__':
    default_images_path = 'static/images/default/'
    DEFAULT_IMAGES = os.listdir(default_images_path)
    check_default_images(DEFAULT_IMAGES, default_images_path)
