import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "👑 **ادمین:** ربات ناشناس 24/7 آنلاین!")
    else:
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton("📩 پیام ناشناس", callback_data="anon")
        markup.add(btn)
        bot.reply_to(message, "🔒 **ربات ناشناس**\n👇 دکمه بزن!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "anon")
def anon_start(call):
    bot.edit_message_text("✍️ **پیام ناشناس بنویس:**", call.message.chat.id, call.message.message_id)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.from_user.id == ADMIN_ID and message.reply_to_message:
        if "[ID:" in message.reply_to_message.text:
            try:
                user_id = int(message.reply_to_message.text.split("[ID:")[1].split("]")[0])
                bot.send_message(user_id, f"💬 **جواب ادمین:**\n\n{message.text}")
                bot.reply_to(message, "✅ **ارسال شد!**")
                return
            except:
                pass
    
    if message.from_user.id != ADMIN_ID:
        markup = InlineKeyboardMarkup()
        btn = InlineKeyboardButton("💬 جواب", callback_data=f"reply_{message.from_user.id}")
        markup.add(btn)
        
        text = f"👤 **ناشناس:**\n\n{message.text}\n\n**ID:** `[ID: {message.from_user.id}]`"
        bot.send_message(ADMIN_ID, text, reply_markup=markup, parse_mode='Markdown')
        bot.reply_to(message, "✅ **پیامت رسید!** ⏳ منتظر جواب...")

print("🔒 ربات ناشناس 24/7 شروع شد!")
bot.infinity_polling()
