import json
import asyncio
import schedule
import time
from datetime import datetime, timedelta
from telegram import Bot
from config import BOT_TOKEN

SUBSCRIBERS_FILE = "subscribers.txt"  # File where all chat_ids are stored

# 1. Load today's full prayer times from local JSON
def get_today_prayer_times():
    today = datetime.today().strftime("%d-%b-%Y")

    with open("prayer_times_2025.json", "r") as f:
        data = json.load(f)

    for day in data["prayerTime"]:
        if day["date"] == today:
            return {
                "Imsak": day["imsak"],
                "Subuh": day["fajr"],
                "Syuruk": day["syuruk"],
                "Dhuha": day["dhuha"],
                "Zohor": day["dhuhr"],
                "Asar": day["asr"],
                "Maghrib": day["maghrib"],
                "Isyak": day["isha"]
            }
    return {}

# 2. Send Telegram alert to all subscribers
async def send_alert(message):
    bot = Bot(token=BOT_TOKEN)
    try:
        with open(SUBSCRIBERS_FILE, "r") as file:
            subscribers = file.read().splitlines()

        for chat_id in subscribers:
            await bot.send_message(chat_id=chat_id, text=message)

    except Exception as e:
        print(f"⚠️ Error sending message: {e}")

# 3. Schedule both 10 minutes before and exact prayer time
def schedule_alert(time_str, name):
    try:
        prayer_time = datetime.strptime(time_str, "%H:%M:%S").time()
    except ValueError:
        print(f"⚠️ Invalid time format for {name}: {time_str}")
        return

    now = datetime.now()
    full_time = datetime.combine(now.date(), prayer_time)
    before_time = full_time - timedelta(minutes=10)

    # Schedule 10 minutes before alert
    schedule.every().day.at(before_time.strftime("%H:%M")).do(
        lambda: asyncio.run(send_alert(f"⏳ 10 mins before {name} ({time_str})"))
    )

    # Schedule at exact prayer time
    schedule.every().day.at(prayer_time.strftime("%H:%M")).do(
        lambda: asyncio.run(send_alert(f"🕌 Time for {name}! ({time_str})"))
    )

# 4. Setup all alerts
def setup_all_alerts():
    times = get_today_prayer_times()
    if not times:
        print("⚠️ No prayer times found for today.")
        return

    print("📅 Today's Solat Times:")
    for name, time_str in times.items():
        print(f"{name}: {time_str}")
        schedule_alert(time_str, name)

# 5. Run scheduler
if __name__ == "__main__":
    print("📅 Setting up today's prayer time alerts...")
    setup_all_alerts()

    print("⏳ Waiting for alerts to trigger...")
    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🛑 Program stopped by user.")
