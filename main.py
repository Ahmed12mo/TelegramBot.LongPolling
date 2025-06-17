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

قاعدة بيانات محلية

DATA_FILE = "data.json" if not os.path.exists(DATA_FILE): with open(DATA_FILE, "w") as f: json.dump({}, f)

def load_data(): with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data): with open(DATA_FILE, "w") as f: json.dump(data, f)

إضافة وثيقة

async def add_document(update: Update, context: ContextTypes.DEFAULT_TYPE): if not update.message.photo: await update.message.reply_text("📎 أرسل صورة مع الأمر من فضلك.") return

name = update.message.text.replace("اضافة", "").strip()
if not name:
    await update.message.reply_text("📝 من فضلك اكتب اسم الوثيقة بعد كلمة 'اضافة'")
    return

file = await update.message.photo[-1].get_file()
file_path = f"downloads/{name.replace(' ', '_')}.jpg"
os.makedirs("downloads", exist_ok=True)
await file.download_to_drive(file_path)

data = load_data()
data[name] = file_path
save_data(data)

await update.message.reply_text(f"✅ تم حفظ الوثيقة باسم: {name}")

البحث عن وثيقة

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE): keyword = update.message.text.replace("بحث", "").strip() data = load_data()

results = [name for name in data if keyword in name]
if results:
    reply = "🔎 تم العثور على الأسماء التالية:\n" + "\n".join(f"✅ {name}" for name in results)
else:
    reply = "❌ لم يتم العثور على نتائج."
await update.message.reply_text(reply)

عرض وثيقة

async def show_document(update: Update, context: ContextTypes.DEFAULT_TYPE): name = update.message.text.replace("وثائق", "").strip() data = load_data()

for key in data:
    if name in key:
        path = data[key]
        with open(path, "rb") as f:
            await update.message.reply_photo(photo=InputFile(f), caption=f"🌸 {key}")
        return

await update.message.reply_text("❌ لم يتم العثور على الوثيقة.")

عرض كل الوثائق

async def list_documents(update: Update, context: ContextTypes.DEFAULT_TYPE): data = load_data() if not data: await update.message.reply_text("📂 لا توجد وثائق محفوظة.") else: msg = "🗂️ الوثائق المحفوظة:\n" + "\n".join(f"✅ {name}" for name in data.keys()) await update.message.reply_text(msg)

حذف وثيقة

async def delete_document(update: Update, context: ContextTypes.DEFAULT_TYPE): name = update.message.text.replace("حذف", "").strip() data = load_data()

for key in list(data):
    if name in key:
        path = data[key]
        if os.path.exists(path):
            os.remove(path)
        del data[key]
        save_data(data)
        await update.message.reply_text(f"🗑️ تم حذف الوثيقة: {key}")
        return

await update.message.reply_text("❌ لم يتم العثور على الوثيقة.")

التوجيه الرئيسي

async def handle_commands(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text.strip() if text.startswith("اضافة"): await add_document(update, context) elif text.startswith("بحث"): await search(update, context) elif text.startswith("وثائق"): await show_document(update, context) elif text.startswith("كل الوثائق"): await list_documents(update, context) elif text.startswith("حذف"): await delete_document(update, context) else: await update.message.reply_text("🤖 أهلاً بك، استخدم الأوامر:

اضافة [اسم] مع صورة

بحث [كلمة]

وثائق [اسم]

كل الوثائق

حذف [اسم]")


# التوجيه الرئيسي
async def handle_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text.startswith("اضافة"):
        await add_document(update, context)
    elif text.startswith("بحث"):
        await search(update, context)
    elif text.startswith("وثائق"):
        await show_document(update, context)
    elif text.startswith("كل الوثائق"):
        await list_documents(update, context)
    elif text.startswith("حذف"):
        await delete_document(update, context)
    else:
        await update.message.reply_text(
            "🤖 أهلاً بك، استخدم الأوامر:\n"
            "🌟 اضافة [اسم] + صورة\n"
            "🔍 بحث [كلمة]\n"
            "📄 وثائق [الاسم]\n"
            "📂 كل الوثائق\n"
            "🗑️ حذف [الاسم]"
        )

# بدء التشغيل
async def start_bot():
    app = ApplicationBuilder().token("7953128215:AAF0CzKGqXWmFsG_TMB6NnJlAmY1J1c5hV4").build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_commands))
    print("✅ البوت يعمل الآن...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(start_bot())
