from telegram.ext import CommandHandler, Updater

from botster.router import Router
from botster.utils import Settings, setup_logger

# Enable logging
logthon = setup_logger(__name__)


def error(update, context):
    """ Log error events
    """

    del update
    del context

    import traceback
    logthon.error(traceback.format_exc())


def main():
    """ Set bot in listening mode and bind bot commands to python handlers
    """

    settings = Settings()

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    # The Updater class continuously fetches new updates from telegram
    # and passes them on to the Dispatcher class.
    # If you create an Updater object, it will create a Dispatcher
    # for you and link them together with a Queue.
    updater = Updater(settings.BOT_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # On different commands - answer in Telegram
    # Every handler is an instance of any subclass of the telegram.ext.Handler class.
    # The library provides handler classes for almost all use cases,
    # but if you need something very specific, you can also subclass Handler yourself.
    router = Router(settings)
    for command in router.commands:
        dp.add_handler(CommandHandler(*command))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
