from collections import namedtuple
from core.ui.uk import uk_dict
from core.ui.en import en_dict


def customDictDecoder(dict1):
    for key, value in dict1.items():
        if type(value) is dict:
            dict1[key] = customDictDecoder(value)
    return namedtuple('X', dict1.keys())(*dict1.values())


ui_text = {}
ui_text.update({"uk": customDictDecoder(uk_dict)})
ui_text.update({"en": customDictDecoder(en_dict)})


