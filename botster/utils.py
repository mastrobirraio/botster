from logthon import Logthon


def setup_logger(module_name=__name__):
    return Logthon(module_name=module_name)


class Settings:

    BOT_KEY = None

    def __init__(self):
        from dotenv import load_dotenv
        from os import getenv as os_get_env_variable

        load_dotenv()
