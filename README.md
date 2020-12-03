# Hikōki
> Hikōki (飛行機) - Plane; Airplane

Hikōki is a Telegram userbot meant for group management, spam handling, and occasionally fun.

## Requirements

* Python 3
* pipenv (`pip3 install pipenv`)
* Some kind of SQL database

Optionally:

* Docker/Podman

## Installation

1. Clone this repo

    ```
    git clone https://github.com/watzon/hikoki.git
    cd hikoki
    ```

2. Install the dependencies

    ```
    pipenv install
    ```

3. Put necessary environment variables into your `.env` file or save them to your local environment. You can ignore `SESSION` for now, but you will need `API_ID` and `API_HASH` which you can get from [my.telegram.org](https://my.telegram.org), and the database information. For more information on the environement variables see below. You will also need to copy `alembic.ini.example` to `alembic.ini` and set the database url there.

4. Sign in with Telegram and generate a session string. We use Telethon's `StringSession` because it's easier to maintain outside of a docker container, and then load in as an environment variable.

    ```
    pipenv run python3 scripts/authorize.py
    ```

5. Set up the database

    ```
    alembic upgrade head
    ```

6. Run the start script.

    ```
    bin/bot
    ```

## Environment

### `API_ID` and `API_HASH`

You can get these from [my.telegram.org](https://my.telegram.org). Your bot **will not** run without them.

### `LOG_CHAT_ID`

The ID of the chat that you want to log things in. You can get this with a bot like `MissRose_bot` or by forwarding a message from that chat/channel to `JsonDumpBot`.

### `SESSION`

The session generated above in step 4 of the installation process.

### `COMMAND_PREFIX`

The prefix to use for commands. Defaults to `.` (period) if this variable isn't set.

### `LOG_FILE`

The file to save logs to

### `LOG_LEVEL`

The log level. Defaults to `WARN`.

### `SPAMWATCH_HOST`

The host to use for the [SpamWatch](https://spamwat.ch) API.

### `SPAMWATCH_API_KEY`

API key for SpamWatch.

### `DB_URL`
The fully qualified url of your database.

### `REPO_URL`
The url for your github repo.
