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

DATA_FILE = "data.json"
ADMIN_ID = 5570934498  # فقط هذا المستخدم يمكنه حذف أو إضافة وثائق

# تحميل البيانات من الملف
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# حفظ البيانات في الملف
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

data = load_data()

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! أرسل صورة + الاسم في الكابشن لحفظها.\n"
                                    "🔍 استخدم: /بحث [اسم] للبحث\n"
                                    "📄 أو /وثائق [الاسم الكامل] لعرض الوثيقة\n"
                                    "📋 أو /كل_الوثائق لعرض جميع الأسماء.")

# حفظ صورة باسم من الكابشن
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.caption:
        return

    name = update.message.caption.strip()
    file_id = update.message.photo[-1].file_id
    data[name] = file_id
    save_data(data)

    await update.message.reply_text(f"✅ تم حفظ الوثيقة باسم: {name}")

# أمر بحث جزئي
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ اكتب اسمًا للبحث.\nمثال: /بحث وليد")
        return

    keyword = " ".join(context.args).lower()
    results = [name for name in data if keyword in name.lower()]

    if results:
        reply = "🔍 النتائج:\n" + "\n".join(f"✅ {name}" for name in results)
    else:
        reply = "❌ لا توجد نتائج."
    await update.message.reply_text(reply)

# عرض وثيقة باسم كامل
async def show_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ اكتب الاسم الكامل.\nمثال: /وثائق وليد محمد العقيدي")
        return

    name = " ".join(context.args)
    if name in data:
        await update.message.reply_photo(photo=data[name], caption=f"📄 الوثيقة: {name}")
    else:
        await update.message.reply_text("❌ لم يتم العثور على الوثيقة.")

# عرض كل الأسماء
async def list_documents(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if data:
        msg = "📋 جميع الوثائق:\n" + "\n".join(f"🌸 {name}" for name in data.keys())
    else:
        msg = "❌ لا توجد وثائق محفوظة."
    await update.message.reply_text(msg)

# حذف وثيقة (أدمن فقط)
async def delete_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 ليس لديك صلاحية هذا الأمر.")
        return

    if not context.args:
        await update.message.reply_text("❗ اكتب الاسم الكامل لحذفه.")
        return

    name = " ".join(context.args)
    if name in data:
        del data[name]
        save_data(data)
        await update.message.reply_text(f"🗑️ تم حذف الوثيقة: {name}")
    else:
        await update.message.reply_text("❌ لا توجد وثيقة بهذا الاسم.")

# إضافة وثيقة يدويًا (أدمن فقط)
async def add_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 ليس لديك صلاحية هذا الأمر.")
        return

    if not context.args or not update.message.photo:
        await update.message.reply_text("❗ استخدم الأمر هكذا:\n/اضف [الاسم] + صورة")
        return

    name = " ".join(context.args)
    file_id = update.message.photo[-1].file_id
    data[name] = file_id
    save_data(data)

    await update.message.reply_text(f"📥 تم إضافة الوثيقة يدويًا: {name}")

# تشغيل البوت
if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN") or "7953128215:AAF0CzKGqXWmFsG_TMB6NnJlAmY1J1c5hV4"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("بحث", search))
    app.add_handler(CommandHandler("وثائق", show_document))
    app.add_handler(CommandHandler("كل_الوثائق", list_documents))
    app.add_handler(CommandHandler("حذف", delete_document))
    app.add_handler(CommandHandler("اضف", add_document))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 البوت يعمل الآن...")
    app.run_polling()
