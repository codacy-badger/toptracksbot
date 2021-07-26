# Top Tracks Bot for Telegram
[![Telegram](https://img.shields.io/badge/telegram-%40toptracksbot-informational)](http://t.me/toptracksbot)
[![Python Version](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)](https://www.python.org/downloads/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/cae4d1afa23240e1a7ca996f7b0d92b8)](https://www.codacy.com/manual/pltnk/toptracksbot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pltnk/toptracksbot&amp;utm_campaign=Badge_Grade)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/pltnk/top_tracks)](https://choosealicense.com/licenses/mit/)

This bot fetches video from YouTube for the top three tracks of all time by specified artist according to Last.fm charts.

The bot is deployed on Heroku and you can try it in Telegram: [@toptracksbot](http://t.me/toptracksbot)

## Deployment

You can deploy this bot yourself using Docker and docker-compose.
1. Install [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
2. Clone this repository
3. Create `.env` file at the root of cloned repo with the following variables declared there:
    - `TTBOT_TOKEN` - Auth token of your Telegram bot [(how to get)](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
    - `TTBOT_LASTFM_API_KEY` - Key for Last.fm API [(how to get)](https://www.last.fm/api)
    - `TTBOT_YOUTUBE_API_KEY` - Key for YouTube API [(how to get)](https://developers.google.com/youtube/v3/getting-started)
    - `TTBOT_DATABASE_USER` - Set a username for the database
    - `TTBOT_DATABASE_PASS` - Set a password for the database 
      
    Check an [example of .env file](./.env_example)
    
4. Start the bot using command `docker-compose up -d` (this will build images for the database and the bot itself and start containers with them)

## Built With
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - This library provides a pure Python interface for the Telegram Bot API.
* [httpx](https://github.com/encode/httpx) - A next-generation HTTP client for Python.
* [asyncpg](https://github.com/MagicStack/asyncpg) - A fast PostgreSQL Database Client Library for Python/asyncio.
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/) - Beautiful Soup is a library that makes it easy to scrape information from web pages. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
