from botster.utils import setup_logger

logthon = setup_logger(module_name=__name__)


class Router:
    """ Class used to get command name and function to bind to Telegram Bot

            Attributes
            ----------------
            commands: list[tuple(str, function,)]
                list of tuples, containing command name and function to bind
    """

    def __init__(self, settings):
        """
        :param settings: Settings instance with all .env parameters and connections
        :type settings: botster.utils.Settings
        """

        self.__settings = settings

    @property
    def commands(self):
        """ list of tuples, containing command name and function to bind

        Reads files inside commands package module and use module name as command name,
        then instance the command class inside module to get reference of function to callback when bots is used.

        :return: list of tuples with command and function to bind
        :rtype: list[tuple(str, function,)]
        """

        import pkgutil

        try:
            import commands
            from botster.utils import Command

            command_base = Command(self.__settings)
        except ImportError:
            logthon.error('No commands dir found')
            return []

        package = commands
        cmds = []
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):

            del importer
            if ispkg:
                continue

            import importlib

            command_module = importlib.import_module("commands." + modname)
            classes = [c for c in dir(command_module) if not c.startswith('_')]
            for c in classes:
                try:
                    command_obj = getattr(command_module, c)(self.__settings)
                    if command_obj.__class__ != command_base.__class__ and hasattr(command_obj, 'execute'):
                        cmds.append((modname, command_obj.telegram_command,))
                except TypeError:
                    pass
        return cmds
