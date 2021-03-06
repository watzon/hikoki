from telethon.errors import UsernameInvalidError, UsernameNotOccupiedError, InviteHashInvalidError

SPAMWATCH_CHAT_ID = -1001275988180

TELEGRAM_DOMAINS = ['t.me',
                    'telegram.org',
                    'telegram.dog',
                    'telegra.ph',
                    'tdesktop.com',
                    'telesco.pe',
                    'graph.org',
                    'contest.dev']

GET_ENTITY_ERRORS = (UsernameNotOccupiedError, UsernameInvalidError,
                     ValueError, InviteHashInvalidError)
