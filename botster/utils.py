import inspect

from logthon import Logthon


def setup_logger(module_name=__name__):
    return Logthon(module_name=module_name)


class Settings:

    BOT_KEY = None

    def __get_attrs(self):
        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        return [a[0] for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]

    def __validate_attrs(self):
        logthon = setup_logger()
        for attr in self.__get_attrs():
            if getattr(self, attr) is None:
                logthon.error(attr + ' is missing in .env')

    def __init__(self):
        from dotenv import load_dotenv
        from os import getenv as os_get_env_variable

        load_dotenv()
        for attr in self.__get_attrs():
            setattr(self, attr, os_get_env_variable(attr))
        self.__validate_attrs()
