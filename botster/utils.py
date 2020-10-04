import inspect

from logthon import Logthon


def setup_logger(module_name=__name__):
    return Logthon(module_name=module_name)


class Settings:
    """ This class is used to get all .env parameters using them as class attributes

            Attributes
            ----------------
            BOT_KEY : str
                Telegram API Token
    """

    BOT_KEY = None

    def __get_attrs(self):
        """ Gets list of attributes name of this class excluding default properties

        :return: The list of attributes name
        :rtype: list
        """

        attributes = inspect.getmembers(self, lambda a: not (inspect.isroutine(a)))
        return [a[0] for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]

    def __validate_attrs(self):
        """ Check if all class attributes are set
        """

        logthon = setup_logger()
        for attr in self.__get_attrs():
            if getattr(self, attr) is None:
                logthon.error(attr + ' is missing in .env')

    def __init__(self):
        """ Sets .env file values as class attributes
        """

        from dotenv import load_dotenv
        from os import getenv as os_get_env_variable

        load_dotenv()
        for attr in self.__get_attrs():
            setattr(self, attr, os_get_env_variable(attr))
        self.__validate_attrs()


class Command:
    """ Simple parent class for all commands

            Attributes
            ----------------
            name : str
                name of Telegram command and file command name
            _context : telegram.ext.Updater
                this is a context object passed to the callback
            _update : telegram.ext.Dispatcher
                dispatches all kinds of updates to its registered handlers
            _bot : telegram.Bot
                represents a Telegram Bot
            _chat_id : int | str
                unique identifier for the target chat or username of the target channel
            _settings : botster.utils.Settings
                object containing all .env values and connections

            Methods
            ----------------
            telegram_command(telegram.ext.Dispatcher, telegram.ext.Updater) : void
                use this method to bind command it with Telegram Bot during routing operations
            execute(): void
                simple parent method to override for command business logics
            _send_message(str) : void
                use this method to send text messages
            _get_attrs() : list[str]
                use this method to get the list of arguments passed to a command
    """

    def __init__(self, settings):
        """
        :param settings: all .env files values and connections
        :type settings: botster.utils.Settings
        """

        self._settings = settings
        self._update = None
        self._context = None

    @property
    def name(self):
        """ Name of Telegram command and file command name.

        Reads instance module name and set it as Telegram Command name.
        Raise AttributeError when command is not define into module package.

        :return: module package name
        :rtype: str
        :raise: AttributeError
        """

        module_package = __name__.split('.')
        if len(module_package):
            return module_package[-1]
        raise AttributeError

    @property
    def _bot(self):
        """ Represents a Telegram Bot

        Gets Bot from Context

        :return: Telegram Bot instance
        :rtype: telegram.Bot
        """

        return self._context.bot

    @property
    def _chat_id(self):
        """ Unique identifier for the target chat or username of the target channel

        Gets identifier from registered handler

        :return: Unique identifier
        :rtype: int | str
        """

        return self._update.effective_chat.id

    def _send_message(self, message):
        """ Use this method to send text messages

        :param message: message to send
        :type message: str
        """

        self._bot.send_message(chat_id=self._chat_id, text=message)

    def _get_args(self):
        """ Use this method to get the list og arguments passed to a command

        :return: list of arguments passed to command
        :rtype: list[str]
        """

        return self._context.args

    def telegram_command(self, update, context):
        """ Use this method to bind command it with Telegram Bot during routing operations

        Gets params from Telegram API and execute the command business logic

        :param update: dispatches all kinds of updates to its registered handlers
        :type update: telegram.ext.Dispatcher

        :param context: this is a context object passed to the callback
        :type context: telegram.ext.Updater
        """

        self._update = update
        self._context = context
        self.execute()

    def execute(self):
        """ Simple parent method to override for command business logics
        """

        logthon = setup_logger()
        logthon.warn('Execute command class is missing')
