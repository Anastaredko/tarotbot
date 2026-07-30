import telebot
import random

BOT_TOKEN = '8783106291:AAGQSNaDMOPJ-Vh4eQz7EXl74v02yqdKGkY'

bot = telebot.TeleBot(BOT_TOKEN)

tarot_cards = [
    {"name": "Маг", "meaning": "Сила воли, мастерство, проявление."},
    {"name": "Жрица", "meaning": "Интуиция, тайна, подсознание."},
    {"name": "Император", "meaning": "Власть, структура, защита."}
]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🔮 Привет! Я твой оракул Таро. Напиши /card, чтобы получить карту дня.")

# Обработчик команды /card
@bot.message_handler(commands=['card'])
def send_tarot_card(message):
    card = random.choice(tarot_cards)
    response = f"🌟 Твоя карта дня: **{card['name']}**\n\n📖 Значение: {card['meaning']}"
    bot.reply_to(message, response)

# Обработчик любого текста (этот сработает, если ни одна команда не подошла)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Я тебя слышу! Напиши /start или /card")

# Запускаем бота
print("🤖 Бот запущен и готов к работе!")
bot.infinity_polling()