from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import random, asyncio

TOKEN = "8601944095:AAHsQTqaDnPWOOF6tXu748QMl6z7NKGgBx4"
ADMIN_ID = 7442476125

groups = set()

gf_bf_replies = [
    "kal raat ko kya maza aaya 😏",
    "kal raat yaad hai na 😈",
    "kal tum bade mood me the 😏🔥",
    "kal ka scene mast tha na 😉",
    "kal tum thode zyada hi close aa rahe the 😈",
    "kal wali baat abhi tak yaad aa rahi hai 😏",
    "kal tum alag hi level pe the 😈🔥",
    "kal tumne to surprise kar diya 😏",
    "kal ke baad tum aur dangerous lag rahe ho 😈",
    "kal tumhare saath time ka pata hi nahi chala 😘",
    "kal wali vibe kuch zyada hi strong thi 😏",
    "kal tum thode control se bahar lag rahe the 😈",
    "kal tumne to pura mood bana diya 😏🔥",
    "kal ke baad se bas tum hi yaad aa rahe ho 😘"
]

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        groups.add(chat.id)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    await asyncio.sleep(random.randint(1,2))

    if "hi" in msg or "hello" in msg:
        await update.message.reply_text("hii jaan 😘 kya kar rahe ho")
    elif "kaisi ho" in msg or "kaise ho" in msg:
        await update.message.reply_text("main thik hu 😊 tum batao miss kar rahe the kya 😏")
    elif "miss" in msg:
        await update.message.reply_text("mujhe bhi tumhari yaad aa rahi thi 😘")
    elif "love" in msg:
        await update.message.reply_text("love you too 😘❤️")
    else:
        await update.message.reply_text(random.choice(gf_bf_replies))

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("message likho")
        return

    msg = " ".join(context.args)

    sent = 0
    for gid in groups:
        try:
            await context.bot.send_message(chat_id=gid, text=msg)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"sent to {sent} groups")

async def groups_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(f"total groups: {len(groups)}")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.add_handler(MessageHandler(filters.ALL, track))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("groups", groups_count))

app.run_polling()
