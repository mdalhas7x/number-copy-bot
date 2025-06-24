
import os from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

ডাটাবেস স্টোর করার জন্য (ইন-মেমোরি)

user_data = {}

✅ Start Command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user keyboard = [ [ InlineKeyboardButton("Main Channel", url="https://t.me/HACKERA17X"), InlineKeyboardButton("Our Group", url="https://t.me/+FVclssxu2fFlOGU9"), ], [InlineKeyboardButton("Done ✅", callback_data="done_join")], ] reply_markup = InlineKeyboardMarkup(keyboard)

text = (
    f"আসসালামু আলাইকুম {user.first_name},\n\n"
    "🤖 আপনাকে আমাদের এই বটে স্বাগতম।\n"
    "✅ বটটি চালু করতে আমাদের চ্যানেল ও গ্রুপে যোগ দিন, তারপর Done বাটনে ক্লিক করুন।\n\n"
    "👤 বট তৈরি করেছেন: @MsSumaiyaKhanom"
)
await update.message.reply_text(text, reply_markup=reply_markup)

✅ Join Check

async def join_check(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query user_id = query.from_user.id await query.answer()

# For simplicity, assume user joined successfully
user_data[user_id] = {
    "numbers": [],
    "copied": 0
}

await query.edit_message_text("✅ Great! Now enter your numbers below:\n(একাধিক নাম্বার দিন এক লাইনে একটাই করে)")

✅ Handle Numbers

async def handle_numbers(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if user_id not in user_data: await update.message.reply_text("❌ দয়া করে /start দিয়ে শুরু করুন।") return

numbers = update.message.text.strip().split("\n")
cleaned = [n.strip() for n in numbers if n.strip()]
user_data[user_id]["numbers"] = cleaned
user_data[user_id]["copied"] = 0

keyboard = [[InlineKeyboardButton("Get Start", callback_data="get_start")]]
await update.message.reply_text(f"✅ {len(cleaned)} টি নাম্বার নেওয়া হয়েছে। নিচে Get Start চাপুন।", reply_markup=InlineKeyboardMarkup(keyboard))

✅ Get Start

async def get_start(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query user_id = query.from_user.id await query.answer()

keyboard = [[InlineKeyboardButton("📋 COPY", callback_data="copy_number")]]
await query.edit_message_text("🟢 নিচে COPY বাটনে ক্লিক করে নাম্বার কপি করুন।", reply_markup=InlineKeyboardMarkup(keyboard))

✅ Copy One Number

async def copy_number(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query user_id = query.from_user.id await query.answer()

data = user_data.get(user_id)
if not data or not data["numbers"]:
    await query.edit_message_text("⚠️ কোনো নাম্বার পাওয়া যায়নি। /start দিয়ে আবার শুরু করুন।")
    return

copied = data["copied"]
if copied >= len(data["numbers"]):
    await query.edit_message_text("🎉 সব নাম্বার কপি শেষ!")
    return

number = data["numbers"][copied]
data["copied"] += 1
total = len(data["numbers"])
left = total - data["copied"]

keyboard = [[InlineKeyboardButton("📋 COPY", callback_data="copy_number")]]
await query.edit_message_text(
    f"📲 {number}\n\n✅ কপি হয়েছে: {data['copied']} টি\n📦 বাকি: {left} টি",
    reply_markup=InlineKeyboardMarkup(keyboard)
)

✅ Delete Command

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if user_id in user_data: user_data[user_id] = {"numbers": [], "copied": 0} await update.message.reply_text("🗑️ আপনার নাম্বার গুলো মুছে ফেলা হয়েছে। এখন আবার নতুন নাম্বার দিন।") else: await update.message.reply_text("❌ আপনি এখনো কোনো নাম্বার দেননি।")

✅ Main Function

def main(): TOKEN = os.getenv("BOT_TOKEN") app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(join_check, pattern="^done_join$"))
app.add_handler(CallbackQueryHandler(get_start, pattern="^get_start$"))
app.add_handler(CallbackQueryHandler(copy_number, pattern="^copy_number$"))
app.add_handler(CommandHandler("delete", delete))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_numbers))

app.run_polling()

if name == 'main': main()

