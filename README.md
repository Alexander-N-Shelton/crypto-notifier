# Crypto Price Notifier for Linux

A Python script that checks current cryptocurrency prices using the CoinMarketCap API and sends a desktop notification with a sound alert. Runs automatically every 15 minutes using a `systemd` user timer.

## Requirements

- Python 3
- `requests`, `pygame`, `python-dotenv`
- A CoinMarketCap API key in a `.env` file.

## Installation

1. Clone or place the script in your desired directory.

2. Create the systemd service and timer files:

    - `~/.config/systemd/user/crypto-notifier.service`

3. Enable and start the timer:

    ```bash
    systemctl --user daemon-reload
    systemctl --user enable --now crypto-notifier.timer
    ```
