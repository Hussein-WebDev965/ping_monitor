import subprocess
import platform
import time
import requests
from datetime import datetime
from config import BOT_TOKEN, CHAT_ID


DEVICES = {
    "Router": "192.168.0.103",
    "Google DNS": "8.8.8.8",
    "Test Fake": "192.168.1.250",
}

CHECK_INTERVAL = 10  # ثواني (للتجربة)

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=10)
    except requests.RequestException as e:
        print(f"فشل إرسال التنبيه: {e}")

def is_alive(host):
    flag = "-n" if platform.system() == "Windows" else "-c"
    result = subprocess.run(
        ["ping", flag, "1", host],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

send_alert("✅ المراقب اشتغل")

last_status = {}  # يحفظ آخر حالة لكل جهاز

while True:
    now = datetime.now().strftime("%H:%M:%S")
    for name, ip in DEVICES.items():
        alive = is_alive(ip)
        print(f"[{now}] {name} ({ip}): {'UP' if alive else 'DOWN'}")

        previous = last_status.get(name)
        if previous is not None and previous != alive:
            if alive:
                send_alert(f"🟢 {name} ({ip}) رجع يشتغل - {now}")
            else:
                send_alert(f"🔴 {name} ({ip}) وقع! - {now}")

        last_status[name] = alive
    print("-" * 40)
    time.sleep(CHECK_INTERVAL)