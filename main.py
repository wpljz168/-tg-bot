# 先自动安装依赖
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])

# 再导入库
import telebot

# 🔑 请把这里替换成你自己的机器人 Token
BOT_TOKEN = "你的机器人Token"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """👋 欢迎使用环球链能商务机器人！

💼 核心功能：
- 链能租赁服务
- 币兑业务办理
- 代理模式申请

请回复以下指令使用服务：
/rent - 租赁链能
/exchange - 币兑业务
/agent - 代理申请""")

# 启动机器人
print("✅ 机器人启动成功！")
bot.infinity_polling()
