from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# 自定义键盘按钮
keyboard = [
    ['🅜 油卡*1张', '🅜 油卡*3张', '🅜 油卡*5张'],
    ['🅜 电信卡*10张', '🅜 电信卡*100张'],
    ['🖨 提取卡密', '👩‍💻 在线客服']
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 每个按钮对应的图片和文字回复
image_text_map = {
    '🅜 油卡*1张': {
        'image_url': 'https://example.com/youka1.jpg',
        'caption': '您选择了油卡1张，请发送订单编号。'
    },
    '🅜 油卡*3张': {
        'image_url': 'https://example.com/youka3.jpg',
        'caption': '您选择了油卡3张，订单已生成。'
    },
    '🅜 油卡*5张': {
        'image_url': 'https://example.com/youka5.jpg',
        'caption': '油卡5张已加入购物车。'
    },
    '🅜 电信卡*10张': {
        'image_url': 'https://example.com/dianxin10.jpg',
        'caption': '电信卡10张，预计5分钟内发货。'
    },
    '🅜 电信卡*100张': {
        'image_url': 'https://example.com/dianxin100.jpg',
        'caption': '您选择了电信卡100张，批量订单处理中。'
    },
    '🖨 提取卡密': {
        'image_url': None,
        'caption': '请输入订单编号以提取卡密。'
    },
    '👩‍💻 在线客服': {
        'image_url': None,
        'caption': '请联系专属客服：@YourAgent'
    }
}

# /start 指令响应
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("欢迎，请选择你需要的卡类：", reply_markup=reply_markup)

# 按钮点击响应
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in image_text_map:
        info = image_text_map[text]
        if info['image_url']:
            await update.message.reply_photo(photo=info['image_url'], caption=info['caption'])
        else:
            await update.message.reply_text(info['caption'])
    else:
        await update.message.reply_text("暂不支持此选项，请联系客服。")

# 启动 bot
app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
app.run_polling()
