import json
import os

TRANSLATE_PATH = os.path.abspath("AgendaBotV2/config/translate_file.json")
LANGUAGES_LIST = ["english", "french"]

def load_translate():
    with open(TRANSLATE_PATH, 'r') as f:
        translation_data = json.load(f)
    return translation_data

def translate(language, tr_type, text):
    if language == 'english' or language == "en":
        return text
    elif language == 'french' or language == "fr":
        try :
            return load_translate()[tr_type][text]
        except KeyError:
            return text
