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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"আসসালামু আলাইকুম {user.mention_html()}\n\n"
        "আপনাকে আমাদের এই বটে স্বাগতম 🥰\n\n"
        "বটটি চালু করতে আমাদের গ্রুপ এবং চ্যানেলে জয়েন হোন তারপর 'Done ✅' বাটনে ক্লিক করুন।"
    )
    buttons = [
        [InlineKeyboardButton("📢 Main Channel", url="https://t.me/HACKERA17X")],
        [InlineKeyboardButton("👥 Our Group", url="https://t.me/+FVclssxu2fFlOGU9")],
        [InlineKeyboardButton("✅ Done", callback_data="check_join")]
    ]
    await update.message.reply_html(text=text, reply_markup=InlineKeyboardMarkup(buttons))

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    try:
        member_channel = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        member_group = await context.bot.get_chat_member(GROUP_ID, user_id)
    except:
        await query.edit_message_text("⚠️ সমস্যা হয়েছে। পরে চেষ্টা করুন।")
        return

    if member_channel.status not in ("left",) and member_group.status not in ("left",):
        user_data[user_id] = {"numbers": [], "index": 0, "last": None}
        await query.edit_message_text("✅ Access Granted!\n\nএখন নাম্বার দিন (লাইন বাই লাইন)।")
    else:
        await query.edit_message_text(
            "❌ প্রথমে আমাদের চ্যানেল এবং গ্রুপে যোগ দিন তারপর আবার চেষ্টা করুন।",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Main Channel", url="https://t.me/HACKERA17X")],
                [InlineKeyboardButton("👥 Our Group", url="https://t.me/+FVclssxu2fFlOGU9")],
                [InlineKeyboardButton("✅ Done", callback_data="check_join")]
            ])
        )

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        await update.message.reply_text("⚠️ প্রথমে /start দিন।")
        return

    numbers = [line.strip() for line in update.message.text.strip().split("\n") if line.strip()]
    if not numbers:
        await update.message.reply_text("⚠️ কোনো নাম্বার পাওয়া যায়নি।")
        return

    user_data[user_id]["numbers"] = numbers
    user_data[user_id]["index"] = 0
    user_data[user_id]["last"] = None

    await update.message.reply_text(
        f"✅ মোট {len(numbers)} টি নাম্বার পাওয়া গেছে।\n\nশুরু করতে নিচের বাটনে চাপ দিন:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Get Start", callback_data="get_start")]
        ])
    )

async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id not in user_data or not user_data[user_id]["numbers"]:
        await query.edit_message_text("⚠️ আগে নাম্বার দিন।")
        return

    await send_next_number(query, user_id)

async def send_next_number(query, user_id):
    data = user_data[user_id]
    index = data["index"]
    numbers = data["numbers"]
    last_number = data["last"]

    if index >= len(numbers):
        await query.edit_message_text("✅ সব নাম্বার কপি শেষ হয়েছে।")
        return

    number = numbers[index]
    data["index"] += 1
    data["last"] = number

    copied = data["index"]
    total = len(numbers)
    remaining = total - copied

    reply_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text=f"📋 {number}", callback_data="copy_number"),
            InlineKeyboardButton(text="👆 Last", callback_data="last_number")
        ],
        [InlineKeyboardButton(f"✅ কপি হয়েছে: {copied}/{total} | ⏳ বাকি: {remaining}", callback_data="status")]
    ])

    await query.edit_message_text(
        text=f"📋 নাম্বার: <code>{number}</code>\n"
             f"✅ কপি হয়েছে: {copied}/{total} টি\n"
             f"⏳ বাকি আছে: {remaining} টি",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def copy_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    await send_next_number(query, user_id)

async def last_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    last = user_data.get(user_id, {}).get("last")
    if not last:
        await query.edit_message_text("❌ আগের কপি নাম্বার পাওয়া যায়নি।")
        return

    await query.edit_message_text(
        text=f"📋 আগের নাম্বার: <code>{last}</code>\n\nআবার কপি করতে চাইলে নিচে চাপ দিন:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"📋 {last}", callback_data="copy_number")]
        ]),
        parse_mode="HTML"
    )

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data.pop(user_id, None)
    await update.message.reply_text("🗑️ আপনার আগের ডেটা মুছে ফেলা হয়েছে।")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("delete", delete))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers))

    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(get_start, pattern="get_start"))
    app.add_handler(CallbackQueryHandler(copy_number, pattern="copy_number"))
    app.add_handler(CallbackQueryHandler(last_number, pattern="last_number"))

    app.run_polling()
