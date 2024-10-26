import telebot

API_TOKEN = '7143628618:AAHHyuHEyUePzIouOyrqfcdxmBXP_AD_ZEo'
print(API_TOKEN)

bot = telebot.TeleBot(
    API_TOKEN
)
print(bot)

@bot.message_handler(commands=['start'])
def send_chat_id(message):
    print(message)
    chat_id = message.chat.id 
    print(chat_id)
    bot.send_message(chat_id, f"Your chat ID is: {chat_id}")

print(0000)

bot.polling(none_stop=True)