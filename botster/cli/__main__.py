import argparse
from os import getcwd

CURRENT_WORK_DIRECTORY = getcwd()
parser = argparse.ArgumentParser('botster-cli args')
parser.add_argument(
    '--start-project',
    metavar='OPTIONAL_PATH',
    nargs='?',
    const=CURRENT_WORK_DIRECTORY,
    type=str,
    help='Scaffold new project. Default current work directory')
args = parser.parse_args()


class CommandLineInterface:
    """ This class is used to manage CLI script args

        METHODS
        ---------------------
        start_project : None | Import and call method to scaffold a new project
        main          : None | Check defined arguments and call related methods
    """

    def __start_project(self):
        """ Import and call method to scaffold a new project
        """

        from botster.cli.scaffold import start_project
        start_project(args.start_project)

    def main(self):
        """ Check defined arguments and call related methods
        """

        if args.start_project:
            self.__start_project()


def execute_from_commandline():
    """ Method called from CLI script
    Is responsible to instance class to handle CLI operations
    """

    utils = CommandLineInterface()
    utils.main()
