from src.Key import Key


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


def set_combination(combination, keys, clicks):
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
