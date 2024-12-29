# Libraries in Clackamas County (LINCC) Culture Pass Notifier

This project is a Python script that uses Selenium to log into the LINCC Culture Pass system, check for available passes, and send notifications via a Telegram bot.

## Prerequisites

- Docker
- Docker Compose
- A Telegram bot token and chat ID

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/lincc-culture-pass-notifier.git
    cd lincc-culture-pass-notifier
    ```

2. Create a `.env` file in the root directory with the following content:
    ```properties
    SELENIUM_HOST=selenium
    SELENIUM_PORT=4444
    BARCODE=12345678
    PIN=1234
    BOT_TOKEN=your_bot_token
    CHAT_ID=your_chat_id
    ```

    **Note:** Use the BARCODE and PIN issued to you during library registration.

## Getting Telegram Bot Token and Chat ID

1. Create a new bot on Telegram by talking to [BotFather](https://t.me/botfather). Follow the instructions to get your bot token.
2. To get your chat ID, you can send a message to your bot and then visit the following URL in your browser:
    ```
    https://api.telegram.org/bot<your_bot_token>/getUpdates
    ```
    Replace `<your_bot_token>` with your actual bot token. Look for the `chat` object in the response to find your chat ID.

## Usage

Run the application using Docker Compose:
```sh
docker-compose up --build -d
```

This command will build the Docker images and start the Selenium container and the application container. The application will automatically use the environment variables from the `.env` file.

## Default Interval

The script is set to run every 10 minutes by default. You can adjust this interval by modifying the cron job settings (crontab file) before using Docker Compose.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Donate

If you find this project useful, consider making a donation to support its development:

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/donate/?business=YUHM53ZPKE6WN&no_recurring=0&item_name=Support+the+Developer%21+%E2%98%95+Buy+me+a+coffee+and+help+fuel+more+great+work%21&currency_code=USD)