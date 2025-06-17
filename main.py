import os
from telebot import TeleBot
from dotenv import load_dotenv
from telebot.types import Message
from telegram import Update, InputFile
from telegram import Update, InputFile
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN')

# Initialize bot
bot = TeleBot(token=TELEGRAM_BOT_TOKEN)


# مجلد لتخزين الصور

# إنشاء مجلد لتخزين الصور
if not os.path.exists("documents"):
    os.makedirs("documents")

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! أرسل صورة ومعها الاسم في الكابشن لحفظ الوثيقة.\n\nواستخدم:\n/بحث الاسم\n/وثائق الاسم")

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

# أمر /بحث
async def handle_arabic_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("/بحث"):
        name = text.replace("/بحث", "").strip()
        file_path = f"documents/{name}.jpg"
        if os.path.exists(file_path):
            await update.message.reply_text(f"✅ موجود: {name}")
        else:
            await update.message.reply_text(f"❌ غير موجود: {name}")

# أمر /وثائق
async def handle_arabic_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("/وثائق"):
        name = text.replace("/وثائق", "").strip()
        file_path = f"documents/{name}.jpg"
        if os.path.exists(file_path):
            await update.message.reply_photo(photo=InputFile(file_path), caption=f"📄 الوثيقة: {name}")
        else:
            await update.message.reply_text(f"❌ لا توجد وثيقة باسم: {name}")

# تشغيل البوت
if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

    app = ApplicationBuilder().token(TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/بحث"), handle_arabic_search))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^/وثائق"), handle_arabic_docs))
    app.add_handler(MessageHandler(filters.PHOTO, save_document))

    print("🤖 البوت يعمل الآن...")
    app.run_polling()
