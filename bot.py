bot.py

import os from telegram import Update, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler)

BOT_TOKEN = os.getenv("BOT_TOKEN") CHANNEL_ID = "@HACKERA17X" GROUP_ID = "-1002129604900"  # Replace with your actual group ID (as integer)

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user keyboard = [ [ InlineKeyboardButton("Main Channel", url="https://t.me/HACKERA17X"), InlineKeyboardButton("Our Group", url="https://t.me/+FVclssxu2fFlOGU9") ], [InlineKeyboardButton("Done ✅", callback_data="check_joined")] ] await update.message.reply_text( f"আসসালামু আলাইকুম {user.first_name},\n" f"আপনাকে আমাদের এই বটে স্বাগতম 🥰\n" f"বটটি চালু করতে নিচের চ্যানেল ও গ্রুপে জয়েন করুন তারপর Done ✅ বাটনে ক্লিক করুন।", reply_markup=InlineKeyboardMarkup(keyboard) )

async def check_joined(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id bot = context.bot

try:
    channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    group_status = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)

    if channel_status.status not in ["left"] and group_status.status not in ["left"]:
        user_data[user_id] = {
            "numbers": [], "copied": 0
        }
        await update.callback_query.message.reply_text("Enter your Numbers\nআপনার নাম্বার গুলো প্রবেশ করান")
    else:
        await update.callback_query.message.reply_text("দয়া করে চ্যানেল এবং গ্রুপে জয়েন করুন আগে।")
except Exception as e:
    await update.callback_query.message.reply_text("সমস্যা হয়েছে। দয়া করে পরে আবার চেষ্টা করুন।")

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id text = update.message.text numbers = [line.strip() for line in text.splitlines() if line.strip()]

if user_id not in user_data:
    await update.message.reply_text("প্রথমে /start কমান্ড দিন।")
    return

user_data[user_id]["numbers"] = numbers
user_data[user_id]["copied"] = 0

await update.message.reply_text(
    f"✅ মোট নাম্বার: {len(numbers)}\nনিচের বাটনে ক্লিক করুন শুরু করতে।",
    reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("Get Start", callback_data="get_start")]]
    )
)

async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if user_id not in user_data or not user_data[user_id]["numbers"]: await update.callback_query.message.reply_text("দয়া করে নাম্বার দিন আগে।") return

await update.callback_query.message.reply_text(
    f"👇 নিচের বাটনে ক্লিক করে একটি একটি করে নাম্বার কপি করুন:",
    reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("COPPY", callback_data="copy_one")]]
    )
)

async def copy_one(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id data = user_data.get(user_id)

if not data or not data["numbers"]:
    await update.callback_query.message.reply_text("নাম্বার নেই! দয়া করে নতুন নাম্বার দিন।")
    return

copied = data["copied"]
if copied >= len(data["numbers"]):
    await update.callback_query.message.reply_text("✅ সব নাম্বার শেষ!")
    return

number = data["numbers"][copied]
data["copied"] += 1
await update.callback_query.message.reply_text(
    f"📞 {number}\n✅ কপি হয়েছে: {data['copied']} টি\n⏳ বাকি: {len(data['numbers']) - data['copied']} টি"
)

async def delete_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id user_data[user_id] = {"numbers": [], "copied": 0} await update.message.reply_text("❌ সব নাম্বার মুছে ফেলা হয়েছে। এখন আবার নতুন নাম্বার দিন।")

if name == 'main': app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("delete", delete_numbers)) app.add_handler(CallbackQueryHandler(check_joined, pattern="check_joined")) app.add_handler(CallbackQueryHandler(get_start, pattern="get_start")) app.add_handler(CallbackQueryHandler(copy_one, pattern="copy_one")) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers)) app.run_polling()


