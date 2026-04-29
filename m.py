import requests, time, asyncio, os, sys
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# ===== CONFIG =====
BOT_TOKEN = "YOUR_BOT_TOKEN"
IMAGEKIT_PRIVATE_KEY = "YOUR_PRIVATE_KEY"
OWNER_ID = 123456789

UPLOAD_URL = "https://upload.imagekit.io/api/v1/files/upload"
start_time = time.time()

# ===== UPLOAD =====
def upload_to_imagekit(file_data, file_name):
    res = requests.post(
        UPLOAD_URL,
        auth=(IMAGEKIT_PRIVATE_KEY, ""),
        files={"file": file_data},
        data={"fileName": file_name}
    ).json()
    return res.get("url"), res.get("fileId")

# ===== DELETE =====
def delete_from_imagekit(file_id):
    requests.delete(
        f"https://api.imagekit.io/v1/files/{file_id}",
        auth=(IMAGEKIT_PRIVATE_KEY, "")
    )

async def auto_delete(file_id):
    await asyncio.sleep(3600)
    delete_from_imagekit(file_id)

# ===== LOADING =====
async def hacker_loading(msg):
    steps = [
        "⚡ Booting system...",
        "📡 Connecting...",
        "🧠 Analyzing...",
        "⚙️ Processing...",
        "🔐 Securing...",
        "🚀 Finalizing..."
    ]
    p = 0
    for s in steps:
        p += 15
        await msg.edit_text(f"{s}\n\n🟩 Progress: {p}%")
        await asyncio.sleep(0.6)

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [["📤 Upload"], ["⏱ Uptime"], ["🔄 Update Bot"]]
    await update.message.reply_text(
        "🔥 Hacker Upload System\n📎 Send file as DOCUMENT for HD",
        reply_markup=ReplyKeyboardMarkup(kb, resize_keyboard=True)
    )

# ===== UPTIME =====
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = int(time.time() - start_time)
    h,m,s = t//3600,(t%3600)//60,t%60
    await update.message.reply_text(f"⏱ {h}h {m}m {s}s")

# ===== UPDATE =====
async def update_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Not allowed")
    msg = await update.message.reply_text("🔄 Updating...")
    res = os.popen("git pull").read()
    await msg.edit_text(f"✅ Updated\n{res}\nRestarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

# ===== TEXT =====
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    if t == "📤 Upload":
        await update.message.reply_text("📎 Send image/file as DOCUMENT")
    elif t == "⏱ Uptime":
        await uptime(update, context)
    elif t == "🔄 Update Bot":
        await update_bot(update, context)

# ===== PHOTO =====
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Send as DOCUMENT for HD")

# ===== DOCUMENT =====
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_all = time.time()

    msg = await update.message.reply_text("⚡ Initializing...")

    doc = update.message.document
    size_bytes = doc.file_size
    size_mb = round(size_bytes/(1024*1024),2)

    # ETA estimate
    assumed_speed = 1.5
    eta = round(size_mb/assumed_speed,2)

    await msg.edit_text(
        f"📡 Upload starting...\n\n"
        f"📦 {size_mb} MB\n"
        f"⚡ ~{assumed_speed} MB/s\n"
        f"⏳ ETA: {eta}s"
    )

    await asyncio.sleep(1)
    await hacker_loading(msg)

    file = await context.bot.get_file(doc.file_id)
    data = requests.get(file.file_path).content

    name = doc.file_name or f"file_{int(time.time())}"

    # upload timing
    up_start = time.time()
    url, file_id = upload_to_imagekit(data, name)
    up_time = round(time.time()-up_start,2)

    # speed
    speed = round(size_mb/up_time,2) if up_time>0 else size_mb

    asyncio.create_task(auto_delete(file_id))

    total = round(time.time()-start_all,2)

    if doc.mime_type and "image" in doc.mime_type:
        final = url+"?tr=w-1536,h-2731,c-maintain_ratio,fo-auto,q-95"
        await msg.edit_text(
            f"╔════════════╗\n"
            f"  ✅ SUCCESS\n"
            f"╚════════════╝\n\n"
            f"📁 {name}\n📦 {size_mb} MB\n\n"
            f"⚡ {speed} MB/s\n"
            f"⏱ Upload: {up_time}s\n"
            f"🧠 Total: {total}s\n\n"
            f"🔥 {final}\n\n"
            f"⏳ Auto delete 1h"
        )
    else:
        await msg.edit_text(
            f"╔════════════╗\n"
            f"  ✅ FILE DONE\n"
            f"╚════════════╝\n\n"
            f"📁 {name}\n📦 {size_mb} MB\n\n"
            f"⚡ {speed} MB/s\n"
            f"⏱ Upload: {up_time}s\n"
            f"🧠 Total: {total}s\n\n"
            f"🔗 {url}\n\n"
            f"⏳ Auto delete 1h"
        )

# ===== RUN =====
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

print("🤖 Running...")
app.run_polling()
