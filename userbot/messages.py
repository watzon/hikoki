from time import strftime, gmtime

date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

INVALID_PHONE = "Error: Invalid phone number\n" \
                "Did you forget your country code?"

BOT_RESTARTED = "Your bot has been restarted.\n" \
                "Started on: %s" % str(date)
