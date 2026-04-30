    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').percent
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())

    await update.message.reply_text(f"""
📊 STATUS
CPU: {cpu}%
RAM: {ram}%
DISK: {disk}%
UPTIME: {str(uptime).split('.')[0]}
""")

# 🔹 UPTIME
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    r = subprocess.run("net stats srv", shell=True, capture_output=True, text=True)
    for line in r.stdout.split("\n"):
        if "Statistics since" in line:
            await update.message.reply_text(line.strip())

# 🔹 SCREENSHOT
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    file = "screen.png"
    os.system(f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $bmp = New-Object Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); $graphics = [Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen(0,0,0,0,$bmp.Size); $bmp.Save('{file}');\"")
    await update.message.reply_photo(photo=open(file, "rb"))
    os.remove(file)

# 🔹 FILE LIST
async def ls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    path = " ".join(context.args) if context.args else "."
    try:
        files = os.listdir(path)
        await update.message.reply_text("\n".join(files[:100]))
    except Exception as e:
        await update.message.reply_text(str(e))

# 🔹 DOWNLOAD
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    if not context.args:
        await update.message.reply_text("Use: /download <path>")
        return
    path = " ".join(context.args)
    if os.path.exists(path):
        await update.message.reply_document(open(path, "rb"))
    else:
        await update.message.reply_text("Not found ❌")

# 🔹 UPLOAD
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    if update.message.document:
        file = await update.message.document.get_file()
        await file.download_to_drive(update.message.document.file_name)
        await update.message.reply_text("Uploaded ✅")

# 🔹 NETWORK
async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    r = subprocess.run("ipconfig", shell=True, capture_output=True, text=True)
    await update.message.reply_text(f"```{r.stdout[:4000]}```", parse_mode="Markdown")

# 🔹 UPDATE
async def update_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    msg = await update.message.reply_text("Updating...")
    subprocess.run("git pull", shell=True)
    await msg.edit_text("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

# 🔹 BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "▶️ COMMAND RUN":
        await update.message.reply_text("Use /aadi <cmd>")
    elif text == "📊 STATUS":
        await status(update, context)
    elif text == "⏱️ UPTIME":
        await uptime(update, context)
    elif text == "📸 SCREENSHOT":
        await screenshot(update, context)
    elif text == "📁 FILES":
        await update.message.reply_text("Use /ls <path>")
    elif text == "🌐 NETWORK":
        await ip(update, context)
    elif text == "🚀 RUN BG":
        await update.message.reply_text("Use /run <command>")
    elif text == "🛑 STOP PROCESS":
        await update.message.reply_text("Use /kill <PID or name>\nCheck /tasks")
    elif text == "🔄 UPDATE":
        await update_bot(update, context)

# 🚀 RUN
app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("aadi", aadi))
app.add_handler(CommandHandler("run", run_cmd))
app.add_handler(CommandHandler("kill", kill))
app.add_handler(CommandHandler("tasks", tasks))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("uptime", uptime))
app.add_handler(CommandHandler("ls", ls))
app.add_handler(CommandHandler("download", download))
app.add_handler(CommandHandler("update", update_bot))
app.add_handler(MessageHandler(filters.Document.ALL, upload))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

print("🔥 BOT RUNNING...")
app.run_polling()
📌 Exit Code: {code}

📄 Output:
{output}

📸 Screenshot below 👇
""")

            # 📸 screenshot
            file = "error.png"
            os.system(f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $bmp = New-Object Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); $graphics = [Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen(0,0,0,0,$bmp.Size); $bmp.Save('{file}');\"")
            await update.message.reply_photo(photo=open(file, "rb"))
            os.remove(file)

    except subprocess.TimeoutExpired:
        await msg.edit_text("❌ TIMEOUT + Screenshot 👇")

        file = "timeout.png"
        os.system(f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $bmp = New-Object Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); $graphics = [Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen(0,0,0,0,$bmp.Size); $bmp.Save('{file}');\"")
        await update.message.reply_photo(photo=open(file, "rb"))
        os.remove(file)

# 🔹 STATUS
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())

    await update.message.reply_text(f"""
📊 STATUS

CPU: {cpu}%
RAM: {ram}%
DISK: {disk}%

UPTIME: {str(uptime).split('.')[0]}
""")

# 🔹 UPTIME
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    r = subprocess.run("net stats srv", shell=True, capture_output=True, text=True)
    for line in r.stdout.split("\n"):
        if "Statistics since" in line:
            await update.message.reply_text(line.strip())

# 🔹 SCREENSHOT
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    file = "screen.png"
    os.system(f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $bmp = New-Object Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); $graphics = [Drawing.Graphics]::FromImage($bmp); $graphics.CopyFromScreen(0,0,0,0,$bmp.Size); $bmp.Save('{file}');\"")
    await update.message.reply_photo(photo=open(file, "rb"))
    os.remove(file)

# 🔹 FILES
async def ls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    path = " ".join(context.args) if context.args else "."
    try:
        files = os.listdir(path)
        await update.message.reply_text("\n".join(files[:100]))
    except Exception as e:
        await update.message.reply_text(str(e))

# 🔹 DOWNLOAD
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    if not context.args:
        await update.message.reply_text("Use: /download <path>")
        return
    path = " ".join(context.args)
    if os.path.exists(path):
        await update.message.reply_document(open(path, "rb"))
    else:
        await update.message.reply_text("Not found ❌")

# 🔹 UPLOAD
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    if update.message.document:
        file = await update.message.document.get_file()
        await file.download_to_drive(update.message.document.file_name)
        await update.message.reply_text("Uploaded ✅")

# 🔹 NETWORK
async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    r = subprocess.run("ipconfig", shell=True, capture_output=True, text=True)
    await update.message.reply_text(f"```{r.stdout[:4000]}```", parse_mode="Markdown")

# 🔹 UPDATE
async def update_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID: return
    msg = await update.message.reply_text("Updating...")
    subprocess.run("git pull", shell=True)
    await msg.edit_text("Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

# 🔹 BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "▶️ COMMAND RUN":
        await update.message.reply_text("Use /aadi <cmd>")

    elif text == "📊 STATUS":
        await status(update, context)

    elif text == "⏱️ UPTIME":
        await uptime(update, context)

    elif text == "📸 SCREENSHOT":
        await screenshot(update, context)

    elif text == "📁 FILES":
        await update.message.reply_text("Use /ls <path>")

    elif text == "🌐 NETWORK":
        await ip(update, context)

    elif text == "🔄 UPDATE":
        await update_bot(update, context)

# 🚀 RUN
app = ApplicationBuilder().token("8472287791:AAEKJPXLNIMSAjg4vW1KSoEipfJ8n_NerSc").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("aadi", aadi))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("uptime", uptime))
app.add_handler(CommandHandler("ls", ls))
app.add_handler(CommandHandler("download", download))
app.add_handler(CommandHandler("update", update_bot))
app.add_handler(MessageHandler(filters.Document.ALL, upload))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

print("🔥 BOT RUNNING...")
app.run_polling()
import subprocess, os, sys, psutil
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

AUTHORIZED_USER_ID = 7512919724

# 🎛️ UI
keyboard = [
    ["▶️ COMMAND RUN"],
    ["📊 STATUS", "⏱️ UPTIME"],
    ["📸 SCREENSHOT"],
    ["📁 FILES", "🌐 NETWORK"],
    ["🚀 RUN BG", "🛑 STOP PROCESS"],
    ["🔄 UPDATE"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# 🔹 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return
    await update.message.reply_text("⚡ Control Panel Ready", reply_markup=markup)

# 🔹 COMMAND RUN (ERROR → SCREENSHOT)
async def aadi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /aadi <command>")
        return

    cmd = " ".join(context.args)
    msg = await update.message.reply_text(f"⚙️ Running:\n{cmd}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        code = result.returncode

        if code == 0:
            output = stdout if stdout else "No output"
            await msg.edit_text(
                f"✅ SUCCESS\n\n💻 Command:\n{cmd}\n\n📌 Exit Code: {code}\n\n📄 Output:\n{output[:3000]}"
            )

        else:
            output = stderr if stderr else stdout if stdout else "Unknown error"
            await msg.edit_text(
                f"❌ ERROR\n\n💻 Command:\n{cmd}\n\n📌 Exit Code: {code}\n\n📄 Output:\n{output[:3000]}\n\n📸 Screenshot below 👇"
            )

            file = "error.png"
            os.system(
                f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; "
                f"$bmp = New-Object Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, "
                f"[System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); "
                f"$graphics = [Drawing.Graphics]::FromImage($bmp); "
                f"$graphics.CopyFromScreen(0,0,0,0,$bmp.Size); "
                f"$bmp.Save('{file}');\""
            )
            await update.message.reply_photo(photo=open(file, "rb"))
            os.remove(file)

    except Exception as e:
        await msg.edit_text(f"❌ EXCEPTION\n\n{str(e)}")

# 🔹 RUN BACKGROUND
async def run_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /run <command>")
        return

    cmd = " ".join(context.args)

    try:
        process = subprocess.Popen(cmd, shell=True)
        await update.message.reply_text(
            f"🚀 STARTED\n\n💻 Command:\n{cmd}\n\n🆔 PID: {process.pid}\n\nUse /kill {process.pid} to stop"
        )
    except Exception as e:
        await update.message.reply_text(str(e))

# 🔹 KILL PROCESS
async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /kill <PID or name>")
        return

    target = context.args[0]

    try:
        if target.isdigit():
            subprocess.run(f"taskkill /F /PID {target}", shell=True)
        else:
            subprocess.run(f"taskkill /F /IM {target}", shell=True)

        await update.message.reply_text(f"🛑 Killed {target} ✅")
    except Exception as e:
        await update.message.reply_text(str(e))

# 🔹 TASKS
async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    r = subprocess.run("tasklist", shell=True, capture_output=True, text=True)
    await update.message.reply_text(r.stdout[:4000])

# 🔹 STATUS
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').percent
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())

    await update.message.reply_text(
        f"📊 STATUS\n\nCPU: {cpu}%\nRAM: {ram}%\nDISK: {disk}%\nUPTIME: {str(uptime).split('.')[0]}"
    )

# 🔹 UPTIME
async def uptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    r = subprocess.run("net stats srv", shell=True, capture_output=True, text=True)
    for line in r.stdout.split("\n"):
        if "Statistics since" in line:
            await update.message.reply_text(line.strip())

# 🔹 SCREENSHOT
async def screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    file = "screen.png"
    os.system(
        f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; "
        f"$bmp = New-Object Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, "
        f"[System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height); "
        f"$graphics = [Drawing.Graphics]::FromImage($bmp); "
        f"$graphics.CopyFromScreen(0,0,0,0,$bmp.Size); "
        f"$bmp.Save('{file}');\""
    )
    await update.message.reply_photo(photo=open(file, "rb"))
    os.remove(file)

# 🔹 FILE LIST
async def ls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    path = " ".join(context.args) if context.args else "."
    try:
        files = os.listdir(path)
        await update.message.reply_text("\n".join(files[:100]))
    except Exception as e:
        await update.message.reply_text(str(e))

# 🔹 DOWNLOAD
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    if not context.args:
        await update.message.reply_text("Use: /download <path>")
        return

    path = " ".join(context.args)

    if os.path.exists(path):
        await update.message.reply_document(open(path, "rb"))
    else:
        await update.message.reply_text("Not found ❌")

# 🔹 UPLOAD
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    if update.message.document:
        file = await update.message.document.get_file()
        await file.download_to_drive(update.message.document.file_name)
        await update.message.reply_text("Uploaded ✅")

# 🔹 NETWORK
async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    r = subprocess.run("ipconfig", shell=True, capture_output=True, text=True)
    await update.message.reply_text(r.stdout[:4000])

# 🔹 UPDATE
async def update_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    msg = await update.message.reply_text("🔄 Updating...")
    subprocess.run("git pull --no-rebase", shell=True)
    await msg.edit_text("♻️ Restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)

# 🔹 BUTTONS
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "▶️ COMMAND RUN":
        await update.message.reply_text("Use /aadi <cmd>")
    elif text == "📊 STATUS":
        await status(update, context)
    elif text == "⏱️ UPTIME":
        await uptime(update, context)
    elif text == "📸 SCREENSHOT":
        await screenshot(update, context)
    elif text == "📁 FILES":
        await update.message.reply_text("Use /ls <path>")
    elif text == "🌐 NETWORK":
        await ip(update, context)
    elif text == "🚀 RUN BG":
        await update.message.reply_text("Use /run <command>")
    elif text == "🛑 STOP PROCESS":
        await update.message.reply_text("Use /kill <PID or name>\nCheck /tasks")
    elif text == "🔄 UPDATE":
        await update_bot(update, context)

# 🚀 RUN
app = ApplicationBuilder().token("8472287791:AAEKJPXLNIMSAjg4vW1KSoEipfJ8n_NerSc").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("aadi", aadi))
app.add_handler(CommandHandler("run", run_cmd))
app.add_handler(CommandHandler("kill", kill))
app.add_handler(CommandHandler("tasks", tasks))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("uptime", uptime))
app.add_handler(CommandHandler("ls", ls))
app.add_handler(CommandHandler("download", download))
app.add_handler(MessageHandler(filters.Document.ALL, upload))
app.add_handler(CommandHandler("update", update_bot))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, buttons))

print("🔥 BOT RUNNING...")
app.run_polling()
