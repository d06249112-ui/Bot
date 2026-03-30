import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔑 Tera BOT TOKEN (baad me change kar lena)
BOT_TOKEN = "8772943006:AAEPhKCX3JbkOqY2SUMgovxuEPg_2sgUK1k"

# 👑 Tera ADMIN ID
ADMIN_ID = 1292053214

user_files = {}
users = set()

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users.add(user_id)
    await update.message.reply_text(
        "👋 Welcome!\n\n📁 Send file to rename"
    )

# FILE RECEIVE
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document

    if not file:
        await update.message.reply_text("❌ Send a file")
        return

    user_id = update.message.from_user.id
    users.add(user_id)

    user_files[user_id] = {
        "file_id": file.file_id,
        "file_name": file.file_name
    }

    await update.message.reply_text("✏️ Send new file name")

# RENAME
async def rename_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_files:
        return

    new_name = update.message.text.strip()
    data = user_files[user_id]

    file_id = data["file_id"]
    old_name = data["file_name"]

    # ✅ Auto extension fix
    ext = ""
    if old_name and "." in old_name:
        ext = old_name.rsplit(".", 1)[-1]

    if "." not in new_name and ext:
        new_name = f"{new_name}.{ext}"

    status = await update.message.reply_text("⏳ Processing...")

    try:
        file = await context.bot.get_file(file_id)
        await file.download_to_drive(new_name)

        await update.message.reply_document(
            document=open(new_name, "rb"),
            filename=new_name,
            caption="✅ Renamed successfully!"
        )

        os.remove(new_name)

        await update.message.reply_text(
            "✨ Thank you for using our bot 😊\n\nSend more files anytime!"
        )

        await status.delete()

    except Exception as e:
        await status.edit_text(f"❌ Error: {e}")

    user_files.pop(user_id, None)

# BROADCAST
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not admin")
        return

    msg = " ".join(context.args)

    if not msg:
        await update.message.reply_text("❌ Write a message")
        return

    count = 0

    for user in users:
        try:
            await context.bot.send_message(chat_id=user, text=msg)
            count += 1
        except:
            pass

    await update.message.reply_text(f"📢 Sent to {count} users")

# APP
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rename_file))

print("🔥 Bot Running...")
app.run_polling()
