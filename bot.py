import os
import telebot
from flask import Flask, request

# Get your bot token from an environment variable (keep your token secure!)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
bot = telebot.TeleBot(token=TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Hello! I am bot')

# Handle all text messages sent to the bot
#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#    try:
#        print(f"Received message: {message.text}")
#        bot.send_message(message.chat.id, "Hello, world!")
#        #bot.reply_to(message, "Hello, world!")
#    except telebot.apihelper.ApiTelegramException as e:
#        print('exception during send', e)
#        if e.error_code == 429:
#            retry_after = int(e.result_json['parameters']['retry_after'])
#            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
#            time.sleep(retry_after)
#            return
#            #echo_all(message)  # Retry the request after waiting

# For webhook support: Use Flask to handle Telegram webhook
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    try:
        json_str = request.stream.read().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        print("Webhook data processed successfully")
    except Exception as e:
        print(f"Error processing webhook: {e}")
    return "!", 200

# Webhook set-up (this is not strictly necessary but it's good practice)
@app.route("/")  # defines what happens when https://telegram-bot-34zs.onrender.com is visited
def webhook():
    bot.remove_webhook()
    print(f"WEBHOOK_URL together with TOKEN is {WEBHOOK_URL}/{TOKEN}")
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    print("Webhook was set")
    return "Webhook set", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))