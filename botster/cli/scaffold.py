#!/usr/bin/env python3

import inspect
from os import listdir
from os.path import dirname, join
from shutil import copy, copytree

from botster import snippet
from botster.utils import Settings, setup_logger

logthon = setup_logger(__name__)


class ScaffoldManager:
    """ This class is used to manage scaffold operations

    Get source folder and snippets folder paths, and copy snippets folder content to source folder

        methods
        ----------------
        scaffold() : void
            main method class that satisfy class scope
    """

    def __init__(self, path):
        """
        :param path: source path, the same where the project will be scaffold
        :type path: str
        """

        self.__path = path

    def __generate_env_file(self):
        """ Generate .env file

        Gets all attributes of Settings class and insert a new a line into .env
        """

        attributes = inspect.getmembers(Settings, lambda a: not (inspect.isroutine(a)))
        attributes = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]

        env_file_name = join(self.__path, '.env')
        with open(env_file_name, 'w') as env_file:
            for attr in attributes:
                env_file.write(attr[0] + '=""\n')

    def scaffold(self):
        """ Main method class that satisfy class scope

        Copy contents of snippets package module inside directory used by user
        then generate the .env file
        """

        src = dirname(snippet.__file__)
        dst = self.__path

        for f in listdir(src):
            filename = join(src, f)
            destination = join(dst, f)
            if f.startswith('__'):
                continue
            try:
                copy(filename, destination)
            except IsADirectoryError:
                copytree(filename, destination)
            except FileNotFoundError:
                logthon.log_and_exit_with_code('Impossible to scaffold directory, source not found', error_code=2)
            except FileExistsError:
                logthon.log_and_exit_with_code('Destination path already exists', error_code=3)

        self.__generate_env_file()


def start_project(path):
    """ Get source directory path and instance Scaffold manager
    """

    logthon.info('Scaffolding new project')
    logthon.info(f'Target directory: {path}')

    manager = ScaffoldManager(path)
    manager.scaffold()
    logthon.success('Project scaffold complete')
