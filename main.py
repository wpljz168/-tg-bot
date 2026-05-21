# 自动安装依赖
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "pyTelegramBotAPI"])

# 导入库
import telebot

# 🔑 已替换为你刚拿到的真实 Token
BOT_TOKEN = "8949385338:AAEK0YNvCjxjgMLhE4KJ8ZVTeQCg_fenmgY"

bot = telebot.TeleBot(BOT_TOKEN)

# /start 指令：发送欢迎菜单
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

# /hello 指令：测试用，确认机器人在线
@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "你好！我是环球链能商务机器人，很高兴为你服务！")

# 启动机器人（后台运行）
print("✅ 机器人启动成功！正在监听消息...")
bot.infinity_polling()
