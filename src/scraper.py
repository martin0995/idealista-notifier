import requests
from bs4 import BeautifulSoup
import json
import time
import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format="|%(levelname)s| %(asctime)s - %(message)s")

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Define the search URL with filters (modify as needed)
IDEALISTA_URL = "https://www.idealista.com/alquiler-viviendas/barcelona-barcelona/con-precio-hasta_1400,metros-cuadrados-mas-de_40,publicado_ultimas-24-horas,alquiler-de-larga-temporada/?ordenado-por=fecha-publicacion-desc"

# Neighborhoods to exclude
EXCLUDED_AREAS = ["Raval", "Gòtic", "Gotico", "Gótico", "Gotic"]

# Track seen listings to avoid duplicates
SEEN_LISTINGS_FILE = "/app/data/seen_listings.json"

def load_seen_listings():
    try:
        with open(SEEN_LISTINGS_FILE, "r") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_seen_listings(seen_listings):
    with open(SEEN_LISTINGS_FILE, "w") as f:
        json.dump(list(seen_listings), f)

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

def send_message_sync(message):
    asyncio.run(send_telegram_message(message))

def scrape_idealista():
    logging.debug(f"Scraping Idealista...")
    print("Scraping Idealista...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(IDEALISTA_URL)

    if response.status_code != 200:
        logging.debug(f"Error fetching page! Status code: {response.status_code}")
        print("Error fetching page! Status code:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    listings = []
    seen_listings = load_seen_listings()

    # Extract each listing
    for listing in soup.find_all("article", class_="item" if "item" in response.text else "listing-item"):  # Adjust class if needed
        try:
            # Title
            title = listing.find("a", class_="item-link").get_text(strip=True)
            link = "https://www.idealista.com" + listing.find("a", class_="item-link")["href"]

            # Description
            description = listing.find("div", class_="description").get_text(strip=True) if listing.find("div", class_="description") else "No description"

            # Extract price
            price_element = listing.find("span", class_="item-price")
            price = price_element.get_text(strip=True).split("€")[0].strip() + " €" if price_element else "No price available"

            # Extract size (m²) and floor
            # Extract item details (rooms, size, floor)
            details_elements = listing.find_all("span", class_="item-detail")

            rooms = details_elements[0].get_text(strip=True) if len(details_elements) > 0 else "Not available"
            size = details_elements[1].get_text(strip=True) if len(details_elements) > 1 else "Not available"
            floor = details_elements[2].get_text(strip=True) if len(details_elements) > 2 else "Not available"

            # Skip if the listing is from an excluded area
            if any(area.lower() in title.lower() or area.lower() in description.lower() for area in EXCLUDED_AREAS):
                continue

            # Check if it's a new listing
            if link not in seen_listings:
                listings.append({
                    "title": title,
                    "link": link,
                    "description": description,
                })
                seen_listings.add(link)

                # Send Telegram notification
                message = f"""🏡 *New Apartment Listing!*\n
📍 {title}\n
💰 {price}
🛏️ {rooms}
📐 {size}
🏢 {floor}\n
🔗 [Click here to view]({link})"""
                send_message_sync(message)

        except Exception as e:
            logging.debug(f"Error parsing listing: {e}")
            print("Error parsing listing:", e)

    save_seen_listings(seen_listings)
    return listings

if __name__ == "__main__":
    while True:
        new_listings = scrape_idealista()
        if new_listings:
            logging.debug(f"Found {len(new_listings)} new listings!")
            print(f"Found {len(new_listings)} new listings!")
        else:
            logging.debug(f"No new listings.")
            print("No new listings.")
        time.sleep(60)  # Wait 1 minutes before scraping again
