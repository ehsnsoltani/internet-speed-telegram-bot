from internet_speed_telegram_bot import InternetSpeedTelegramBot



# create an object from InternetSpeedTelegramBot Class
bot = InternetSpeedTelegramBot()

# Get the internet speed of your connection
bot.get_internet_speed()
upload_speed = bot.up
donwload_speed = bot.down
text = f"Your Download speed is {donwload_speed} And your Upload speed is {upload_speed}"

# send the message to telegram
bot.send_message_at_telegram(message=text)





