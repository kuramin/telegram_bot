import os
import telebot
from flask import Flask, request

# Get your bot token from an environment variable (keep your token secure!)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Handle all text messages sent to the bot
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Hello, world!")

# For webhook support: Use Flask to handle Telegram webhook
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.stream.read().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# Webhook set-up (this is not strictly necessary but it's good practice)
@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("WEBHOOK_URL") + TOKEN)
    return "Webhook set", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))