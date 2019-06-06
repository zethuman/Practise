import os
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

INITIAl, MIDDLE, FINAL = range(3)

def start(bot, updater):
    updater.message.reply_text('Hello')
    return INITIAl


def say_hello(bot, updater):
    updater.message.reply_text('I am in INITIAL state')
    return MIDDLE


def say_howdy(bot, updater):
    updater.message.reply_text('I am in MIDDLE state')
    return FINAL


def say_good_bye(bot, updater):
    updater.message.reply_text('I am in FINAL state, goodbye')


def cancel(bot, updater):
    updater.message.reply_text('Good bye')
    return ConversationHandler.END


def help(bot, updater):
    updater.message.reply_text('Bot started')


def main():
    TOKEN = os.environ['TELEGRAM_TOKEN']
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher
    command = CommandHandler('help', help)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states= { INITIAl: [MessageHandler(Filters.text, say_hello), CommandHandler('init', start)],
                  MIDDLE: [MessageHandler(Filters.text, say_howdy)],
                  FINAL: [MessageHandler(Filters.text, say_good_bye)]},
        fallbacks= [CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(command)

    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
    updater.bot.set_webhook("https://zethumanbot.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()