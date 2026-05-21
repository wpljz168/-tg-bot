import telebot
import requests
import threading
import time
import uuid
import os

BOT_TOKEN = "8742859360:AAGe1GsXCX1cBzgHliFe8vUV0ZxJGg_stec"
API_KEY = ""
API_BASE = "https://api.eopen.io/api/v1/tron/energy"

MY_TRX_ADDR = "TPCAT7VbB7kuGeBtwvVwMcJzRpURYJMDb6"
MY_USDT_ADDR = "TPCAT7VbB7kuGeBtwvVwMcJzRpURYJMDb6"
ADMIN_ID = 8015227954

bot = telebot.TeleBot(BOT_TOKEN)
headers = {"API-KEY": API_KEY}
user_session = {}
wait_pay_order = {}

def get_order_id():
    return f"HL{uuid.uuid4().hex[:12].upper()}"

@bot.message_handler(content_types=['new_chat_members'])
def welcome(msg):
    txt = """🎉欢迎加入环球链能能量服务站
主营：TRX能量租赁｜币币兑换｜全网招商
资金直达个人账户，安全靠谱
全天自助下单，极速秒出单
私聊机器人发送 /start 即可下单咨询"""
    bot.send_message(msg.chat.id, txt)

@bot.message_handler(commands=["规则"])
def group_rule(msg):
    rule = """📢群内管理条例
1.本群专注能量业务交流，禁止无关闲聊
2.严禁广告、外链、低俗违规内容
3.禁止冒充管理私下交易，谨防被骗
4.一切交易认准官方机器人与群主
违规直接清理，望大家互相理解"""
    bot.send_message(msg.chat.id, rule)

@bot.message_handler(commands=["start"])
def home_menu(msg):
    menu = """👋您好，欢迎来到环球链能服务中心
💼主营业务
1.波场TRX能量租赁
2.大额能量批量代充
3.USDT↔TRX快速兑换
4.全国代理招商合作

📱快捷指令
/rent 能量租赁下单
/exchange 币兑业务
/order 订单查询
/agent 代理政策
/help 下单教程"""
    bot.send_message(msg.chat.id, menu)

@bot.message_handler(commands=["help"])
def help_text(msg):
    help_txt = """📝标准下单流程
1.发送 /rent 进入下单页面
2.选择能量数量+租赁时长
3.填写自己接收能量钱包地址
4.按金额转账至我方收款地址
5.转账完成发送 已付款+订单号
6.管理员核实后自动安排发放"""
    bot.send_message(msg.chat.id, help_txt)

@bot.message_handler(commands=["rent"])
def rent_enter(msg):
    price_info = """⚡能量租赁报价表
65000能量 小额应急
100000能量 日常够用
500000能量 批量使用
1000000能量 商户专供

时长可选：1小时/3小时/12小时/24小时
格式发送：数量 时长
示例：100000 1小时"""
    user_session[msg.from_user.id] = {"step":1}
    bot.send_message(msg.chat.id, price_info)

@bot.message_handler(func=lambda m: user_session.get(m.from_user.id,{}).get("step")==1)
def get_num_time(msg):
    try:
        data = msg.text.strip().split()
        num = int(data[0])
        t_time = data[1]
        user_session[msg.from_user.id] = {"step":2,"num":num,"time":t_time}
        bot.send_message(msg.chat.id,"请发送您接收能量的波场钱包地址(T开头)")
    except:
        bot.send_message(msg.chat.id,"格式错误！请按照示例发送：100000 1小时")

@bot.message_handler(func=lambda m: user_session.get(m.from_user.id,{}).get("step")==2)
def create_order(msg):
    uid = msg.from_user.id
    addr = msg.text.strip()
    info = user_session[uid]
    order_id = get_order_id()
    if info["num"] == 100000:
        price = 12
    elif info["num"] == 500000:
        price = 56
    elif info["num"] == 1000000:
        price = 108
    else:
        price = round(info["num"]/8300,2)
    wait_pay_order[order_id] = {
        "uid":uid,
        "num":info["num"],
        "time":info["time"],
        "addr":addr,
        "money":price,
        "status":"待付款"
    }
    order_txt = f"""✅订单创建成功
订单编号：{order_id}
租赁能量：{info['num']}
租赁时长：{info['time']}
应付金额：{price} TRX

💳付款地址
{MY_TRX_ADDR}
转账成功后发送：已付款 {order_id} 等待审核放款"""
    bot.send_message(msg.chat.id,order_txt)
    user_session.pop(uid,None)

@bot.message_handler(func=lambda m: "已付款" in m.text)
def pay_notify(msg):
    text = msg.text.strip()
    for oid in wait_pay_order.keys():
        if oid in text:
            od = wait_pay_order[oid]
            notice = f"""🔔新订单待审核
订单号：{oid}
租赁能量：{od['num']}
应付金额：{od['money']}TRX
客户地址：{od['addr']}
核实到账回复：确认放款 {oid}"""
            bot.send_message(ADMIN_ID,notice)
            od["status"] = "已付款待审核"
            bot.send_message(msg.chat.id,"已收到付款通知，管理员核实后立即安排发放，请耐心等待~")
            return
    bot.send_message(msg.chat.id,"未查询到对应订单号，请核对无误后重新发送")

@bot.message_handler(func=lambda m: m.from_user.id==ADMIN_ID and "确认放款" in m.text)
def admin_send(msg):
    text = msg.text.strip()
    for oid in wait_pay_order.keys():
        if oid in text:
            od = wait_pay_order[oid]
            od["status"] = "已完成放款"
            success_txt = f"🎉订单{oid}已审核完成，能量已成功发放至您钱包，请查收！"
            bot.send_message(od["uid"],success_txt)
            bot.send_message(msg.chat.id,f"已成功为订单{oid}完成放款")
            return
    bot.send_message(msg.chat.id,"订单编号错误，核对后重试")

@bot.message_handler(commands=["order"])
def search_order(msg):
    bot.send_message(msg.chat.id,"请发送完整订单编号查询")
    @bot.message_handler(func=lambda x:True)
    def res(x):
        oid = x.text.strip()
        if oid in wait_pay_order:
            d = wait_pay_order[oid]
            res_txt = f"""📄订单详情
订单号：{oid}
租赁数量：{d['num']}
租赁时长：{d['time']}
订单状态：{d['status']}"""
            bot.send_message(x.chat.id,res_txt)
        else:
            bot.send_message(x.chat.id,"暂无此订单信息")

@bot.message_handler(commands=["exchange"])
def exchange_biz(msg):
    ex_txt = """💱币币兑换业务
实时汇率参考
1USDT≈12.6 TRX
1TRX≈0.079 USDT
支持大批量快速兑换
全款现货结算，安全稳定
需要兑换直接私聊管理洽谈"""
    bot.send_message(msg.chat.id,ex_txt)

@bot.message_handler(commands=["agent"])
def agent_invite(msg):
    agent_txt = """🤝环球链能诚招全网代理
1.零门槛入驻，无需囤货垫资
2.高额下级返佣，客源永久绑定
3.独立收款，资金自己掌控
4.全套运营话术+机器人免费扶持
5.稳定一手货源，价格优势大
有意向直接私聊对接详细政策"""
    bot.send_message(msg.chat.id,agent_txt)

@bot.message_handler(func=lambda m:True)
def auto_key(m):
    txt = m.text.lower()
    if "租能量" in txt or "价格" in txt:
        rent_enter(m)
    elif "兑换" in txt or "换币" in txt:
        exchange_biz(m)
    elif "代理" in txt:
        agent_invite(m)

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            time.sleep(3)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
