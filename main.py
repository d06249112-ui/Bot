import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8772943006:AAEPhKCX3JbkOqY2SUMgovxuEPg_2sgUK1k"
ADMIN_ID = 1292053214

user_files = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome!\n\n📁 Send me any file to rename.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document
    user_files[update.message.from_user.id] = file
    await update.message.reply_text("✏️ Send new file name (with extension)\nExample: movie.mp4")

async def rename_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_files:
        return

    new_name = update.message.text
    file = user_files[user_id]

    file_obj = await context.bot.get_file(file.file_id)
    file_path = f"{new_name}"

    await file_obj.download_to_drive(file_path)

    await update.message.reply_document(document=open(file_path, "rb"))

    os.remove(file_path)
    del user_files[user_id]

    await update.message.reply_text("✅ File renamed successfully!\n\n🙏 Thank you for using this bot ❤️")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    msg = " ".join(context.args)

    for user in user_files.keys():
        try:
            await context.bot.send_message(chat_id=user, text=msg)
        except:
            pass

    await update.message.reply_text("📢 Broadcast sent!")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rename_file))

    print("🔥 Bot Running...")

    app.run_polling()

if __name__ == "__main__":
    main()
