# Transport Telegram Bot

## Project Description
This project is a Telegram bot that allows you to get the current Minsk bus schedule using data from the website [btrans.by](https://minsk.btrans.by/). The bot parses the schedule, processes user requests and returns information that is convenient for viewing in Telegram.

## Features
- **Getting a schedule:** Parsing current data from the Btrans website.
- **Processing user requests:** Entering a route number (for example, "11" or "9d") to get a schedule.

## Requirements
- Python 3.7+
- Internet connection
- Dependencies from requirements.txt

## Installation
1. **Clone the repository**:
    ```bash
    git clone https://github.com/roma9302/transport_bot.git
    cd transport_bot

2. **Create and activate the virtual environment:**
      ```bash
      python -m venv venv
      source venv/bin/activate # For Windows: venv\Scripts\activate

3. **Install dependencies:**
      ```bash
      pip install -r requirements.txt

4. **Configuration:**

    Get a token for your bot via BotFather.

    in the config/settings.py file, insert your token into the TOKEN constant

    Make sure that the token file is not included in public repositories (use .gitignore for the config.py file).

      ```bash
      TOKEN = "Your token"

5. **Running the bot:**
    To run the bot, run the command:
      ```bash
      python -m scr.bot.bot

## Development
Schedule parsing: The parsing logic is implemented using requests and BeautifulSoup4. The file responsible for parsing can be found in the parser.py module.

Integration with Telegram API: The bot uses the aiogram library and separates the logic of command processing from schedule parsing.

## Contribution and support
If you find a bug or want to suggest improvements, create an issue or pull request in this repository.

## License
This project is distributed under the MIT license. Please see LICENSE for details.
