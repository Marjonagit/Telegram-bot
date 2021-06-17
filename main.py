import logging

import requests
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler
from telegram.ext.filters import Filters
from telegram.update import Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

import settings

updater = Updater(token='1840913092:AAE_6XfurlMJdvX2SXaA2UotP0DsYhxkj1U')


def start(update: Update, context: CallbackContext):
    update.message \
        .reply_text('Hi. This bot shows you the latest weather')


def search(update: Update, context: CallbackContext):
    args = context.args

    logging.info('checking args length')

    if len(args) == 0:
        update.message \
            .reply_text('Enter the name of the place'
                        '/search Rome')
    else:
        search_text = ' '.join(args)
        logging.info('sending request to Weather API')
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', {
            'appid': '4de8a578d7a6c6fe2bdd98537047ae2f',
            'search': search_text,
            
        })

        logging.info('result from Weather API')
        result = response.json()
        link = result[3]

        if len(link):
            update.message \
                .reply_text('Search request: ' + link[0])
        else:
            update.message \
                .reply_text('Nothing has been found')


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('search', search))
dispatcher.add_handler(MessageHandler(Filters.all, start))

updater.start_polling()
updater.idle()
