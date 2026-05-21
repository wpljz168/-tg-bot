import telebot

BOT_TOKEN = "8949385338:AAEK0YNvCjxjgMLhE4KJ8ZVTeQCg_fenmgY"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 欢迎使用环球链能商务机器人！")

bot.infinity_polling()
