import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "-1002188107100"
GROUP_ID = "-1002213974388"

user_data = {}

WELCOME_TEXT = (
    "আসসালামু আলাইকুম {name}\n\n"
    "আপনাকে আমাদের এই বটে স্বাগতম 🥰\n"
    "বটটি চালু করতে আমাদের গ্রুপ এবং চ্যানেলে জয়েন হোন তারপর 'Done ✅' বাটনে ক্লিক করুন।"
)

START_BUTTONS = [
    [
        InlineKeyboardButton("📢 Main Channel", url="https://t.me/HACKERA17X"),
        InlineKeyboardButton("👥 Our Group", url="https://t.me/+FVclssxu2fFlOGU9")
    ],
    [InlineKeyboardButton("✅ Done", callback_data="check_join")]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = WELCOME_TEXT.format(name=user.mention_html())
    await update.message.reply_html(
        text=text,
        reply_markup=InlineKeyboardMarkup(START_BUTTONS)
    )

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    try:
        member_channel = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        member_group = await context.bot.get_chat_member(GROUP_ID, user_id)
    except:
        await query.edit_message_text("⚠️ কিছু সমস্যা হয়েছে। দয়া করে পরে আবার চেষ্টা করুন।")
        return

    if member_channel.status in ["member", "administrator", "creator"] and \
       member_group.status in ["member", "administrator", "creator"]:
        user_data[user_id] = {"numbers": [], "index": 0}
        await query.edit_message_text(
            "✅ Access Granted!\n\nEnter your Numbers:\nআপনার নাম্বার গুলো প্রবেশ করান"
        )
    else:
        await query.edit_message_text(
            "❌ দয়া করে গ্রুপ এবং চ্যানেলে যোগ দিন এবং আবার 'Done ✅' বাটনে ক্লিক করুন।",
            reply_markup=InlineKeyboardMarkup(START_BUTTONS)
        )

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        await update.message.reply_text("দয়া করে প্রথমে /start দিন।")
        return

    numbers = update.message.text.strip().split("\n")
    numbers = [n.strip() for n in numbers if n.strip()]
    user_data[user_id]["numbers"] = numbers
    user_data[user_id]["index"] = 0

    await update.message.reply_text(
        f"✅ মোট {len(numbers)} টি নাম্বার এন্টার হয়েছে।",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🚀 Get Start", callback_data="get_start")]]
        )
    )

async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "👍 শুরু করা হলো! এখন 'COPY' বাটনে চাপ দিন।",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📋 COPY", callback_data="copy_number")]]
        )
    )

async def copy_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in user_data or not user_data[user_id]["numbers"]:
        await query.edit_message_text("❌ নাম্বার পাওয়া যায়নি। প্রথমে নাম্বার দিন।")
        return

    index = user_data[user_id]["index"]
    numbers = user_data[user_id]["numbers"]

    if index < len(numbers):
        number = numbers[index]
        user_data[user_id]["index"] += 1
        copied = user_data[user_id]["index"]
        total = len(numbers)
        remaining = total - copied

        await query.edit_message_text(
            f"📋 নাম্বার: {number}\n✅ কপি হয়েছে: {copied}/{total} টি\n⏳ বাকি আছে: {remaining} টি",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📋 COPY", callback_data="copy_number")]]
            )
        )
    else:
        await query.edit_message_text("✅ সব নাম্বার কপি শেষ হয়েছে।")

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_data:
        user_data.pop(user_id)
        await update.message.reply_text("🗑️ আপনার আগের নাম্বার গুলো ডিলিট হয়েছে।\nআবার নাম্বার দিন:")
    else:
        await update.message.reply_text("❌ কিছুই পাওয়া যায়নি ডিলিট করার মতো।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(get_start, pattern="get_start"))
    app.add_handler(CallbackQueryHandler(copy_number, pattern="copy_number"))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers))

    app.run_polling()
