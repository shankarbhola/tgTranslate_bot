from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters
from googletrans import Translator

# Replace 'YOUR_BOT_TOKEN' with your actual bot token obtained from BotFather on Telegram
BOT_TOKEN = '6804339186:AAEPamHDnjlTPb48QCWi4lbRfaLNx_mVPK0'

# Initialize the translator
translator = Translator()
print("Bot Started")
# Start command handler
def start(update: Update, _: CallbackContext) -> None:
    keyboard = [
        # [InlineKeyboardButton("English to Hindi", callback_data='hi')],
        # [InlineKeyboardButton("Hindi to English", callback_data='en')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hi! I am Language Translation Bot. Send me a message and click the button to translate it.", reply_markup=reply_markup)

# Translate message based on button click
def translate_button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    lang_code = query.data
    translated_text = translator.translate(query.message.text, dest=lang_code).text
    query.answer()
    query.edit_message_text(text=f"{translated_text}")
print("Bot running")
# Message handler for non-button messages
def translate_text(update: Update, _: CallbackContext) -> None:
    message = update.message.text
    input_language = translator.detect(message).lang
    print(input_language)
    if input_language=="hi":
        translated_text = translator.translate(message, dest="en").text
        update.message.reply_text(f"{translated_text}")
    elif input_language=="en":
        translated_text = translator.translate(message, dest="hi").text
        update.message.reply_text(f"{translated_text}")

# Main function to set up the bot
def main() -> None:
    updater = Updater(BOT_TOKEN)

    # Add handlers
    updater.dispatcher.add_handler(CallbackQueryHandler(translate_button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
