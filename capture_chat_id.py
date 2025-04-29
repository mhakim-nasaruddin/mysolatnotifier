# capture_chat_id.py

# 1. Import libraries
import asyncio
import nest_asyncio  # <- Import this immediately
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

from config import BOT_TOKEN

# 2. Apply nest_asyncio immediately to fix Windows event loop
nest_asyncio.apply()

# 3. Subscribers storage
SUBSCRIBERS_FILE = "subscribers.txt"

# 4. Function to save new subscriber
async def save_chat_id(update: Update, context):
    chat_id = update.message.chat.id

    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            subscribers = f.read().splitlines()

        if str(chat_id) not in subscribers:
            with open(SUBSCRIBERS_FILE, "a") as f:
                f.write(str(chat_id) + "\n")
            print(f"✅ New subscriber saved: {chat_id}")
        else:
            print(f"🔵 Existing subscriber: {chat_id}")

    except FileNotFoundError:
        with open(SUBSCRIBERS_FILE, "w") as f:
            f.write(str(chat_id) + "\n")
        print(f"✅ New subscriber saved: {chat_id}")

# 5. Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_chat_id))

    print("📥 Bot is running to capture subscribers...")
    await app.run_polling()

# 6. Start program
if __name__ == "__main__":
    asyncio.run(main())
