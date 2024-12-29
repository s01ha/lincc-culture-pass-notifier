#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import argparse
from argparse import RawTextHelpFormatter

import urllib.parse
import time
import os
import json
from datetime import datetime
import requests

def arguments():
    parser = argparse.ArgumentParser(description="LINCC.org Culture Pass Notifier.", formatter_class=RawTextHelpFormatter)
    parser.add_argument("--selenium-host", metavar="SELENIUM_HOST", help="set the selenium host url (without http).")
    parser.add_argument("--selenium-port", metavar="SELENIUM_PORT", help="set the selenium port.")
    parser.add_argument("--barcode", metavar="BARCODE", help="set the barcode of your LINCC account.")
    parser.add_argument("--pin", metavar="PIN", help="set the pin of your LINCC account.")
    parser.add_argument('--bot-token', type=str, required=True, help='The bot token for the Telegram bot.')
    parser.add_argument('--chat-id', type=str, required=True, help='The chat ID to send images to.')
    return parser.parse_args()

def create_driver(args):
    # Create and configure the Selenium WebDriver
    if args.selenium_host is None:
        print('You should set the host url of selenium.')
        return None
    else:
        print(f'Selenium Host: {args.selenium_host}')
        print(f'Selenium Port: {args.selenium_port}')

        selenium_host = "http://" + args.selenium_host.split("://")[-1]
        selenium_port = int(args.selenium_port) if args.selenium_port is not None else 4444
        selenium_url = urllib.parse.urljoin(base=f'{selenium_host}:{selenium_port}', url='wd/hub', allow_fragments=True)
        
        print(f'Selenium: {selenium_url}')
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Remote(
            command_executor=selenium_url,
            options=chrome_options
        )
        driver.implicitly_wait(3)
        return driver

def load_activities():
    # Load activities from the activities.json file
    activities_file_path = os.path.join(os.path.dirname(__file__), "activities.json")
    if not os.path.exists(activities_file_path):
        return [
            {
                "name": "Pittock Mansion",
                "max_date": "2025-01-10"
            },
        ]
    else:
        with open(activities_file_path, "r", encoding="utf-8") as file:
            activities = json.load(file)
            print(f"Activities: {activities}")
            return activities

def login(driver, args, login_url):
    # Log into the LINCC.org Culture Pass system
    driver.get(login_url)
    time.sleep(5)

    barcode_field = driver.find_element(By.ID, "ePASSPatronNumber")
    pin_field = driver.find_element(By.ID, "ePASSPatronPassword")

    barcode_field.send_keys(args.barcode)
    pin_field.send_keys(args.pin)
    pin_field.send_keys(Keys.RETURN)
    time.sleep(5)

    print("Login successful")

def check_activity(driver, activity, bot_token, chat_id):
    # Check the availability of a specific activity
    all_attractions_button = driver.find_element(By.ID, "ePASSAllAttractionsAnchor")
    all_attractions_button.click()
    time.sleep(5)

    activity_offer_button = driver.find_element(By.XPATH, f"//span[contains(text(), '{activity["name"]}')]/following::a[contains(text(), 'Show first available offer')]")
    activity_offer_button.click()
    time.sleep(5)

    if not driver.find_elements(By.XPATH, f"//span[contains(text(), '{activity['name']}')]"):
        print(f"{activity['name']} not found on the page. Skipping to next activity.")
        return

    print(f"{activity['name']}'s offer page loaded")

    available_date_element = driver.find_element(By.XPATH, "//span[contains(@class, 'ePASSCurrentDate')]")
    available_date = available_date_element.text
    available_date_formatted = datetime.strptime(available_date, "%B %d, %Y").strftime("%Y-%m-%d")
    print(f"{activity['name']}'s Available Date: {available_date_formatted}")

    if available_date_formatted <= activity["max_date"]:
        message = f"{activity['name']}: {available_date_formatted}"
        print(message)

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(url, data=data)
        response.raise_for_status()
    else:
        print(f"{activity['name']}: Not available until {activity['max_date']}")

def main() -> None:
    args = arguments()
    LOGIN_URL = 'https://culturalpassexpress.quipugroup.net/'

    driver = create_driver(args)
    if driver is None:
        return

    activities = load_activities()

    try:
        login(driver, args, LOGIN_URL)

        for activity in activities:
            check_activity(driver, activity, args.bot_token, args.chat_id)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()    

if __name__ == "__main__":
    main()
