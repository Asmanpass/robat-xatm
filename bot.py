import os
import requests
import asyncio
from datetime import datetime
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from threading import Thread

# ترفند رایگان ماندن در Render با Flask
app_flask = Flask('')

@app_flask.route('/')
def home():
    return "Bot is alive and running!"

def run_web():
    app_flask.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

def keep_alive():
    t = Thread(target=run_web)
    t.start()

TOKEN = "8929264370:AAGATTmUY8zewFLpvFutpgWUxDt4mHuBQsM"
GOOGLE_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyk4NBwuxnyZ5Ku1nQ7Qa3X6ty3pjZcIeUTwWFnr_pCXFBU6xXpNrMICHeBVC2wBWBk/exec"

MINI_APP_URL = "https://asmanpass.github.io/baneh-quran-app/"
POSTER_URL = "https://tangerine-yeot-c65e22.netlify.app"
AZAN_URL = "https://asmanpass.github.io/azan"
CHANNEL_URL = "https://t.me/quran_bane"
ADMIN_URL = "@sinazarefar"

def to_persian_num(num_str):
    if num_str is None:
        return ''
    persian_digits = str.maketrans('0123456789', '۰۱٢۳۴۵۶۷۸۹')
    return str(num_str).translate(persian_digits)

def get_sheet_data():
    try:
        response = requests.get(GOOGLE_WEB_APP_URL, timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("Error fetching sheet data:", e)
    return None

def get_dynamic_location_message():
    data = get_sheet_data()
    
    # مقادیر پیش‌فرض امن در صورت عدم اتصال به شیت
    mosque_name = "مزگەوتی دیاریکراو"
    final_juz = 1
    start_date_str = None

    if data:
        mosque_name = data.get("mosque", "مزگەوتی دیاریکراو")
        manual_juz = data.get("manualJuz")
        start_date_str = data.get("startDate")

        if manual_juz:
            try:
                final_juz = int(manual_juz)
            except:
                pass
        elif start_date_str:
            try:
                start_date = datetime.strptime(str(start_date_str).split("T")[0], "%Y-%m-%d")
                now = datetime.now()
                diff_weeks = abs((now - start_date).days) // 7
                final_juz = (diff_weeks % 30) + 1
            except:
                pass

    kurdish_ordinals = [
        'یەکەم', 'دووهەم', 'سێیەم', 'چوارەم', 'پێنجەم', 'شەشەم', 'حەوتەم', 'هەشتەم', 'نۆیەم', 'دەیەم', 
        'یانزەیەم', 'دوانزەیەم', 'سیانزەیەم', 'چواردەیەم', 'پازدەیەم', 'شازدەیەم', 'حەڤدەیەم', 'هەژدەیەم', 
        'نۆزدەیەم', 'بیستەم', 'بیست و یەکەم', 'بیست و دووهەم', 'بیست و سێیەم', 'بیست و چوارەم', 
        'بیست و پێنجەم', 'بیست و شەشەم', 'بیست و حەوتەم', 'بیست و هەشتەم', 'بیست و نۆیەم', 'سییەم'
    ]
    juz_word = kurdish_ordinals[final_juz - 1] if 1 <= final_juz <= 30 else to_persian_num(final_juz)

    msg = (
        "<b>📍 ناونیشانی مزگەوتی ئەم هەفتەیە:</b>\n\n"
        f"<b>🕌 {mosque_name}</b>\n\n"
        f"<b>📖 تیلاوەتی: جوزئی {juz_word} ({to_persian_num(final_juz)})</b>\n\n"
        "<b>⏰ کات: چوارشەممە، دوای نوێژی عیشا</b>"
    )
    return msg

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "<b>✨ بەناوی خودا. بەخێربێن بۆ ڕۆباتی کۆڕی خەتمی قوڕئانی پیرۆز لە شاری بانە.</b>\n\nتکایە بۆ بینینی بەرنامەی هەفتانە، پۆستەری مەراسیم یان کاتی بانگ، کلیک لەسەر دوگمەکانی خوارەوە بکە:"
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
    await update.message.reply_text(msg, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📱 کردنەوەی بەرنامەی هەفتانە", web_app=WebAppInfo(url=MINI_APP_URL))]]
    await update.message.reply_text("<b>📱 بۆ کردنەوەی بەرنامەی هەفتانە (مینی‌ئەپ) کلیک لە سەر دوگمەی خوارەوە بکە:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def poster_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🕌 پۆستەری مەراسیم", web_app=WebAppInfo(url=POSTER_URL))]]
    await update.message.reply_text("<b>🕌 بۆ بینینی پۆستەری مەراسیم کلیک لە سەر دوگمەی خوارەوە بکە:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def azan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🕰 کاتی بانگ بە ئاسۆی بانە", web_app=WebAppInfo(url=AZAN_URL))]]
    await update.message.reply_text("<b>🕰 بۆ بینینی کاتی بانگ بە ئاسۆی شاری بانە کلیک لە سەر دوگمەی خوارەوە بکە:</b>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard))

async def location_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = get_dynamic_location_message()
    await update.message.reply_text(msg, parse_mode="HTML")

async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"<b>📢 لینکی کەناڵی فەرمی کۆڕی خەتمی قورئان:</b>\n\n<b>👉 {CHANNEL_URL}</b>"
    await update.message.reply_text(msg, parse_mode="HTML")

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"<b>📞 بۆ پەیوەندی گرتن لەگەڵ بەڕێوەبەرانی کۆڕ، دەتوانن نامە بۆ ئەم ئایدییە بنێرن:</b>\n\n👤<b> {ADMIN_URL}</b>"
    await update.message.reply_text(msg, parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "<b>💡 ڕێنمایی بەکارهێنان:</b>\n\n<b>ئەم ڕۆباتە بۆ ئاگاداربوون لە بەرنامەی هەفتانەی خەتمی قوڕئانی پیرۆز لە شاری بانە دروست کراوە. بە لێدانی دوگمەی مینی‌ئەپ، دەتوانیت کات، شوێن، جوز‌ء و ناوی قوڕئانخوێنەکان ببینی.</b>"
    await update.message.reply_text(msg, parse_mode="HTML")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "loc":
        msg = get_dynamic_location_message()
        await query.message.reply_text(msg, parse_mode="HTML")
    elif query.data == "hlp":
        msg = "<b>💡 ڕێنمایی بەکارهێنان:</b>\n\n<b>ئەم ڕۆباتە بۆ ئاگاداربوون لە بەرنامەی هەفتانەی خەتمی قوڕئانی پیرۆز لە شاری بانە دروست کراوە.</b>"
        await query.message.reply_text(msg, parse_mode="HTML")

async def main_async():
    keep_alive()
    app = Application.builder().token(TOKEN).build()

    # ثبت تمامی دستورات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("app", app_command))
    app.add_handler(CommandHandler("poster", poster_command))
    app.add_handler(CommandHandler("azan", azan_command))
    app.add_handler(CommandHandler("location", location_command))
    app.add_handler(CommandHandler("channel", channel_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("ربات پایتون با تمامی دستورات فعال شد...")
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    while True:
        await asyncio.sleep(3600)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
