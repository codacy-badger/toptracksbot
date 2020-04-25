"""
This module is a part of Top Tracks Bot for Telegram
and is licensed under the MIT License.
Copyright (c) 2019-2020 Kirill Plotnikov
GitHub: https://github.com/pltnk/toptracksbot
"""


import asyncio
import logging
import os

from requests.exceptions import HTTPError
from telegram import ChatAction
from telegram.ext import CommandHandler, MessageHandler, Updater
from telegram.ext.filters import Filters

import fetching
import storing


TOKEN = os.getenv("BOT_TOKEN")
MODE = os.getenv("BOT_MODE")
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP = os.getenv("HEROKU_APP")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def start(update, context):
    """Process /start command that sent to the bot."""
    logging.info(
        f'(start) Incoming message: args={context.args}, text="{update.message.text}"'
    )
    context.bot.send_message(
        chat_id=update.message.chat_id, text="Enter an artist or a band name."
    )


def send_top(update, context):
    """Process incoming message, send top tracks by the given artist or send an error message."""
    logging.info(
        f'(send_top) Incoming message: args={context.args}, text="{update.message.text}"'
    )
    keyphrase = update.message.text
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=ChatAction.TYPING
    )
    try:
        top = asyncio.run(storing.process(keyphrase))
        for youtube_id in top:
            context.bot.send_message(
                chat_id=update.message.chat_id, text=f"youtube.com/watch?v={youtube_id}"
            )
    except HTTPError as e:
        logging.error(e)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"An error occurred, most likely I couldn't find this artist on Last.fm."
            f"\nMake sure this name is correct.",
        )


def send_info(update, context):
    """Process /info command."""
    logging.info(
        f'(send_info) Incoming message: args={context.args}, text="{update.message.text}"'
    )
    if len(context.args) == 0:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Command must be followed by artist name.\nExample: /info Nirvana",
        )
    else:
        keyphrase = " ".join(context.args)
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=ChatAction.TYPING
        )
        info = asyncio.run(fetching.get_info(keyphrase))
        context.bot.send_message(chat_id=update.message.chat_id, text=info)


def send_help(update, context):
    """Process /help command."""
    logging.info(
        f'(send_help) Incoming message: args={context.args}, text="{update.message.text}"'
    )
    message = (
        "Enter an artist or a band name to get their top three tracks of all time "
        "according to last.fm charts.\n/info <artist> - get short bio of an artist\n/help - show this message."
    )
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def unknown(update, context):
    """Process any unknown command."""
    logging.info(
        f'(unknown) Incoming message: args={context.args}, text="{update.message.text}"'
    )
    context.bot.send_message(
        chat_id=update.message.chat_id, text="Unknown command, try /help."
    )


def main():
    # initialize updater
    updater = Updater(token=TOKEN, use_context=True)
    # updater that uses proxy
    # REQUEST_KWARGS = {'proxy_url': 'http://195.189.96.213:3128'}
    # updater = Updater(token=TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    # initialize handlers
    start_handler = CommandHandler("start", start)
    top_handler = MessageHandler(Filters.text & (~Filters.command), send_top)
    info_handler = CommandHandler("info", send_info)
    help_handler = CommandHandler("help", send_help)
    unknown_handler = MessageHandler(Filters.command, unknown)

    # add handlers to dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(top_handler)
    dispatcher.add_handler(info_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(unknown_handler)

    # start bot
    try:
        if MODE == "prod":
            updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN)
            updater.bot.set_webhook(f"https://{HEROKU_APP}.herokuapp.com/{TOKEN}")
        else:
            logging.info("Starting bot")
            updater.start_polling()
            updater.idle()
    except Exception as e:
        logging.error(f"Unable to start a bot. {e}")


if __name__ == "__main__":
    main()
