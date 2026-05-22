import os
import telebot
from telebot import types

# 从环境变量读取Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ 错误：BOT_TOKEN 变量未配置！请在部署平台的环境变量里添加BOT_TOKEN")
    exit(1)

# 初始化机器人
bot = telebot.TeleBot(BOT_TOKEN)

# /start指令回复
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ 欢迎使用环球链服务！\n\n发送 /start 开始使用，或直接发送消息咨询。")

# 兜底回复，处理所有其他消息
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "请发送 /start 开始使用机器人服务！")

# 启动机器人，断线自动重连
if __name__ == "__main__":
    print("🤖 机器人运行中，等待消息...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"⚠️  连接异常，正在重试：{e}")
            continue
