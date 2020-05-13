#!/usr/bin/env python3

from botster.utils import setup_logger

logthon = setup_logger(__name__)


class ScaffoldManager:
    """ This class is used to manage scaffold operations

    Get source folder and snippets folder paths, and copy snippets folder content to source folder

        ATTRIBUTES
        ----------------
        path     : str  | source path, the same where the project will be scaffold

        METHODS
        ----------------
        scaffold : None | main method class that satisfy class scope
    """

    def __init__(self, path):
        self.__path = path

    def scaffold(self):
        from os import listdir
        from os.path import dirname, join
        from shutil import copy, copytree

        from botster import snippet

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


def start_project():
    """ Get source directory path and instance Scaffold manager
    """
    from os import getcwd

    path = getcwd()

    logthon.info('Scaffolding new project')
    logthon.info(f'Target directory: {path}')

    manager = ScaffoldManager(path)
    manager.scaffold()
    logthon.success('Project scaffold complete')
