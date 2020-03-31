# Hikōki
> Hikōki (飛行機) - Plane; Airplane

Hikōki is a Telegram userbot meant for group management, spam handling, and occasionally fun.

## Requirements

- [x] Python 3
- [x] pipenv (`pip3 install pipenv`)
- [x] Server running MongoDB

Optionally:

- [x] Docker/Podman

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

3. Put necessary environment variables into your `.env` file or save them to your local environment. You can ignore `SESSION` for now, but you will need `API_ID` and `API_HASH` which you can get from [my.telegram.org](https://my.telegram.org), and the database information. For more information on the environement variables see below.

4. Sign in with Telegram and generate a session string. We use Telethon's `StringSession` because it's easier to maintain outside of a docker container, and then load in as an environment variable.

    ```
    pipenv run python3 scripts/authorize.py
    ```

5. For running locally save the generated session string to your `.env` file, otherwise save it as an environment variable.

6. Run the start script.

    ```
    bin/bot
    ```

## Docker / Podman

If you have docker or podman installed the process becomes much easier. You'll still need the environment variables, but once you have them loaded you can just run:

```
docker build -t hikoki .
# or
podman build -t hikoki .
```

and then

```
docker run hikoki
#or
podman run hikoki
```

Alternately you can set up a docker-compose like [this](./docker-compose.example.yml).

## Environment

### `API_ID` and `API_HASH`

You can get these from [my.telegram.org](https://my.telegram.org). Your bot **will not** run without them.

### `LOG_CHAT_ID`

The ID of the chat that you want to log things in. You can get this with a bot like `MissRose_bot` or by forwarding a message from that chat/channel to `JsonDumpBot`.

### `SESSION`

The session generated above in step 4 of the installation process.

### `MONGO_DB_URI`

The connection URI for your MongoDB instance. You can create a free databse using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

### `MONGO_DB_NAME`

The name of the database.

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
