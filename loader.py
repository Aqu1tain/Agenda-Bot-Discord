##################################
# Loader Python from Json config #
##################################

import json
import os
from translater import LANGUAGES_LIST

CONFIG_PATH = os.path.abspath("AgendaBotV2/config/config.json")

def load_config():
    """
    Loads the configuration from the 'config.json' file.
    
    Returns:
        dict: The loaded configuration as a dictionary.
    """
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config["config"]

def data_tuple(array=load_config()):
    """
    Generate a tuple containing the TOKEN and CHANNEL_ID from the given array.

    Parameters:
        array (dict): Optional. The array containing the TOKEN and CHANNEL_ID.
                      If not provided, the default value is loaded from the config file.

    Returns:
        tuple: A tuple containing the TOKEN and CHANNEL_ID.
    """
    return (array["TOKEN"], array["CHANNEL_ID"])

def get_language():
    """
    Loads the language from the 'config.json' file.

    Returns:
        str: The language as a string.
    """
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config["config"]["language"]

def change_language(language):
    """
    Changes the language in the 'config.json' file.

    Parameters:
        language (str): The new language as a string.

    Returns:
        None
    """
    if language in LANGUAGES_LIST:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        config["config"]["language"] = language
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
    else:
        raise ValueError(f"Invalid language: {language}")

def get_moderator_role():
    """
    Loads the moderator role from the 'config.json' file.

    Returns:
        str: The moderator role as a string.
    """
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    return config["config"]["moderator_role"]

def change_moderator_role(role):
    """
    Changes the moderator role in the 'config.json' file.

    Parameters:
        role (str): The new moderator role as a string.

    Returns:
        None
    """
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
    config["config"]["moderator_role"] = role
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)