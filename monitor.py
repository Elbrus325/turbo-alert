import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://turbo.az/autos?q%5Bmodel%5D%5B%5D=4089&q%5Bsort%5D=date"

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )

def get_ads():
    headers = {
        "User-Agent": "Mozilla/5.0 (Android 15) AppleWebKit/537.36 Chrome/140 Mobile Safari/537.36"
    }

    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    ads = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if not href.startswith("/autos/"):
            continue

        link = "https://turbo.az" + href

        if link in [x["link"] for x in ads]:
            continue

        text = a.get_text(" ", strip=True)

        if not text:
            continue

        ads.append({
            "link": link,
            "text": text
        })

    return ads[:20]


def main():
    ads = get_ads()

    if not ads:
        print("Elan tapılmadı.")
        return

    first = ads[0]

    message = (
        "🚨 TURBO.AZ YENİ ELAN TESTİ\n\n"
        f"{first['text']}\n\n"
        f"🔗 {first['link']}"
    )

    send_telegram(message)
    print("Telegram mesajı göndərildi.")


if __name__ == "__main__":
    main()
