import os
import telebot
from flask import Flask, request

# Get your bot token from an environment variable (keep your token secure!)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
bot = telebot.TeleBot(token=TOKEN, threaded=False)
app = Flask(__name__)

#@bot.message_handler(commands=['start']) # welcome message handler. Works with start command only
#def send_welcome(message):  # this name can be anything
#    print(f"reply Hello Im bot to {message}") 
#    bot.reply_to(message, 'Hello! I am bot')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        print(f"Received message: {message.text}")
        bot.reply_to(message, "Hello, world! is what I say to every message")
    except telebot.apihelper.ApiTelegramException as e:
        print('exception during answering:', e)

# For webhook support: Use Flask to handle Telegram webhook
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    try:
        json_str = request.stream.read().decode('UTF-8')
        print(f"json_str is {json_str}")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        print("Webhook data processed successfully")
        return "!", 200
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return e
    
# Webhook set-up (this is not strictly necessary but it's good practice)
@app.route("/webhook", methods=["POST"])  # defines what happens when https://telegram-bot-34zs.onrender.com/webhook is visited
def reset_webhook_from_envvars():  # somehow it was also launched right after going live
    bot.remove_webhook()
    print(f"WEBHOOK_URL together with TOKEN is {WEBHOOK_URL}/{TOKEN}")
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    print("Webhook was reset")
    return "Webhook set", 200

if __name__ == "__main__":
    reset_webhook_from_envvars()
    #print(f"WEBHOOK_URL together with TOKEN is {WEBHOOK_URL}/{TOKEN}")
    #bot.remove_webhook()
    #bot.set_webhook(url=f"{WEBHOOK_URL}/{TOKEN}")
    #print("Webhook was set from inside main")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)), debug=True)