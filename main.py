import os
import telebot

# 从Railway读取Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("错误：BOT_TOKEN 变量未配置！")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# /start指令回复
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ 环球链能商务机器人已启动！\n欢迎使用能量租赁服务！")

# 兜底回复，处理所有其他消息
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "请发送 /start 启动机器人")

# 启动机器人，断线自动重连
if __name__ == "__main__":
    print("机器人运行中，等待消息...")
    bot.polling(none_stop=True)
