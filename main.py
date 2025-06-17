import os
from telebot import TeleBot
from dotenv import load_dotenv
from telebot.types import Message
from telegram import Update, InputFile
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')

# Initialize bot
bot = TeleBot(token=TELEGRAM_BOT_TOKEN)


# مجلد لتخزين الصور
if not os.path.exists("documents"):
    os.makedirs("documents")

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! أرسل صورة ومعها الاسم في الكابشن لحفظ الوثيقة.")

# حفظ الصور
async def save_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message.caption:
        await message.reply_text("❗ رجاءً أضف اسم الوثيقة في الكابشن.")
        return

    name = message.caption.strip()
    file = await message.photo[-1].get_file()
    file_path = f"documents/{name}.jpg"
    await file.download_to_drive(file_path)

    await message.reply_text(f"✅ تم حفظ الوثيقة باسم: {name}")

# البحث عن اسم
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("🔍 استخدم الأمر هكذا:\n/بحث الاسم")
        return

    name = " ".join(context.args)
    file_path = f"documents/{name}.jpg"

    if os.path.exists(file_path):
        await update.message.reply_text(f"✅ تم العثور على {name}")
    else:
        await update.message.reply_text(f"❌ لم يتم العثور على {name}")

# إرسال الوثائق
async def send_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("📂 استخدم الأمر هكذا:\n/وثائق الاسم")
        return

    name = " ".join(context.args)
    file_path = f"documents/{name}.jpg"

    if os.path.exists(file_path):
        await update.message.reply_photo(photo=InputFile(file_path), caption=f"📄 الوثيقة: {name}")
    else:
        await update.message.reply_text(f"❌ لا توجد وثيقة باسم: {name}")

# تشغيل البوت
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("بحث", search))
    app.add_handler(CommandHandler("وثائق", send_document))
    app.add_handler(MessageHandler(filters.PHOTO, save_document))

    print("🤖 البوت يعمل الآن...")
    app.run_polling()

bot.infinity_polling()
