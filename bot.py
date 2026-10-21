import os
import asyncio
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from threading import Thread

# ترفند رایگان ماندن در Render با Flask
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# تنظیمات ربات
TOKEN = "8929264370:AAGATTmUY8zewFLpvFutpgWUxDt4mHuBQsM"

MINI_APP_URL = "https://asmanpass.github.io/baneh-quran-app/"
POSTER_URL = "https://asmanpass.github.io/pooster/"
AZAN_URL = "https://asmanpass.github.io/azan"
CHANNEL_URL = "https://t.me/quran_bane"
ADMIN_URL = "https://t.me/sinazarefar"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "<b>✨ بەناوی خودا. بەخێربێن بۆ ڕۆباتی کۆڕی خەتمی قوڕئانی پیرۆز لە شاری بانە.</b>\n\n"
        "تکایە بۆ بینینی بەرنامەی هەفتانە، پۆستەری مەراسیم یان کاتی بانگ، کلیک لەسەر دوگمەکانی خوارەوە بکە:"
    )
    keyboard = [
        [InlineKeyboardButton("✨ 📱 کردنەوەی بەرنامەی هەفتانە ✨", web_app=WebAppInfo(url=MINI_APP_URL))],
        [InlineKeyboardButton("🕌 پۆستەری مەراسیم", web_app=WebAppInfo(url=POSTER_URL))],
        [InlineKeyboardButton("🕰 کاتی بانگ بە ئاسۆی بانە", web_app=WebAppInfo(url=AZAN_URL))],
        [
            InlineKeyboardButton("📍 مزگەوت", callback_data="loc"),
            InlineKeyboardButton("🌐 کەناڵ", url=CHANNEL_URL)
        ],
        [
            InlineKeyboardButton("💡 ڕێنمایی", callback_data="hlp"),
            InlineKeyboardButton("🧑‍💻 ئەدمین", url=ADMIN_URL)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=reply_markup)

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📱 کردنەوەی بەرنامەی هەفتانە", web_app=WebAppInfo(url=MINI_APP_URL))]]
    await update.message.reply_text("<b>📱 بۆ کردنەوەی بەرنامەی هەفتانە (مینی‌ئەپ) کلیک لە سەر دوگمەی خوارەوە بکە:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def azan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🕰 کاتی بانگ بە ئاسۆی بانە", web_app=WebAppInfo(url=AZAN_URL))]]
    await update.message.reply_text("<b>🕰 بۆ بینینی کاتی بانگ بە ئاسۆی شاری بانە کلیک لە سەر دوگمەی خوارەوە بکە:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "loc":
        loc_msg = "<b>📍 ناونیشانی مزگەوتی ئەم هەفتەیە:</b>\n\n<b>🕌 مزگەوتی دیاریکراو</b>\n\n<b>⏰ کات: چوارشەممە، دوای نوێژی عیشا</b>"
        await query.message.reply_text(loc_msg, parse_mode="HTML")
    elif query.data == "hlp":
        hlp_msg = "<b>💡 ڕێنمایی بەکارهێنان:</b>\n\n<b>ئەم ڕۆباتە بۆ ئاگاداربوون لە بەرنامەی هەفتانەی خەتمی قوڕئانی پیرۆز دروست کراوە.</b>"
        await query.message.reply_text(hlp_msg, parse_mode="HTML")

def main():
    # روشن کردن سرور وب سبک برای پلن رایگان
    keep_alive()
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("app", app_command))
    app.add_handler(CommandHandler("azan", azan_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("ربات پایتون روی وب سرویس رایگان روشن شد...")
    app.run_polling()

if __name__ == "__main__":
    main()
