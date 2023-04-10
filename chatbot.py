from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import ChatGPT
import configparser
import logging
import redis
import os

global redis1
global gptapi

def main():
	global redis1
	global gptapi
	# Load your token and create an Updater for your Bot

	# config = configparser.ConfigParser()
	# config.read('config.ini')
	# updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
	# # redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']),
	# # 					 port=(config['REDIS']['REDISPORT']))
	# redis1 = redis.Redis(
	# 	host=(config['REDIS']['HOST']),
	# 	password=(config['REDIS']['PASSWORD']),
	# 	port=(config['REDIS']['REDISPORT']),
	# 	db=0,
	# 	ssl=True,
	# 	ssl_cert_reqs=None
	# )
	# gptapi = (config['OPENAI']['GPTAPIKEY'])


	updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
	# redis1 = redis.Redis(host=(os.environ['HOST']), password=(os.environ['PASSWORD']), port=(os.environ['REDISPORT']))
	redis1 = redis.Redis(
		host=(os.environ['HOST']),
		port=(os.environ['REDISPORT']),
		db=0,
		password=(os.environ['PASSWORD']),
		ssl=True,
		ssl_cert_reqs=None
	)
	gptapi = os.environ['GPTAPIKEY']

	# print(redis1.ping())
	if not redis1.ping():
		print("redis server down")



	dispatcher = updater.dispatcher
	# You can set this logging module, so you will know when and why things do not work as expected
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
	# register a dispatcher to handle message: here we register an echo dispatcher
	echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
	dispatcher.add_handler(echo_handler)
	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("add", add))
	dispatcher.add_handler(CommandHandler("help", help_command))
	dispatcher.add_handler(CommandHandler("hello", hello))
	dispatcher.add_handler(CommandHandler('history', history_handler))
	dispatcher.add_handler(CommandHandler('clear', clear))
	# dispatcher.add_handler(CommandHandler("c", gpt))
	# To start the bot:
	updater.start_polling()
	updater.idle()


def echo(update, context: CallbackContext) -> None:
	# reply_message = update.message.text.upper()
	# logging.info("Update: " + str(update))
	# logging.info("context: " + str(context))
	# context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
	# Define a few command handlers. These usually take the two arguments update and
	# context. Error handlers also receive the raised TelegramError object in error.
	try:
		msg = update.message.text
		redis1.rpush('message_history', msg)
		logging.info("Update: " + str(update))
		logging.info("context: " + str(context))
		reply_message = ChatGPT.GPT_req(msg, gptapi)
		if reply_message != "" or None:
			context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
		else:
			context.bot.send_message(chat_id=update.effective_chat.id, text="GPT isn't working, please try it again")
	except (IndexError, ValueError):
		update.message.reply_text('')


def help_command(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /help is issued."""
	update.message.reply_text('Helping you helping you.')


def hello(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /hello is issued."""
	msg = context.args[0]  # /add keyword <-- this should store the keyword
	update.message.reply_text(('Good day, ' + msg + '!'))


def add(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /add is issued."""
	try:
		global redis1
		logging.info(context.args[0])
		msg = context.args[0]	# /add keyword <-- this should store the keyword
		redis1.incr(msg)
		update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
	except (IndexError, ValueError):
		update.message.reply_text('Usage: /add <keyword>')


def history_handler(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /history is issued."""
	# Get the message history from Redis
	message_history = redis1.lrange('message_history', 0, -1)
	# Send the message history back to the user
	if len(message_history) == 0:
		message_history = ["History is empty."]
		context.bot.send_message(chat_id=update.effective_chat.id, text=message_history[0])
	else:
		message_history_text = "\n".join([message.decode('utf-8') for message in message_history])
		context.bot.send_message(chat_id=update.effective_chat.id, text=message_history_text)


def clear(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /clear is issued."""
	redis1.flushdb()
	update.message.reply_text('Chat history cleared.')


if __name__ == '__main__':
	main()
