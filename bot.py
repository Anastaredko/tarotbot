import telebot
import random
import os
import sqlite3
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ========== НАСТРОЙКИ ==========
BOT_TOKEN = '8783106291:AAGQSNaDMOPJ-Vh4eQz7EXl74v02yqdKGkY'

bot = telebot.TeleBot(BOT_TOKEN)

# ========== ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ ==========
def init_db():
    conn = sqlite3.connect('tarot_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            card_name TEXT,
            card_suit TEXT,
            card_meaning TEXT,
            card_number TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_user_card(user_id, card_name, card_suit, card_meaning, card_number):
    conn = sqlite3.connect('tarot_bot.db')
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, card_name, card_suit, card_meaning, card_number, date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, card_name, card_suit, card_meaning, card_number, today))
    
    conn.commit()
    conn.close()

def get_user_card(user_id):
    conn = sqlite3.connect('tarot_bot.db')
    cursor = conn.cursor()
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT card_name, card_suit, card_meaning, card_number, date
        FROM users
        WHERE user_id = ? AND date = ?
    ''', (user_id, today))
    
    result = cursor.fetchone()
    conn.close()
    return result

init_db()

# ========== ВСЕ КАРТЫ ТАРО ==========
all_cards = [
    {"name": "Шут", "suit": "Старшие Арканы", "meaning": "Начало нового пути. Доверься своему энтузиазму."},
    {"name": "Маг", "suit": "Старшие Арканы", "meaning": "Сила воли, мастерство, проявление. Действуй!"},
    {"name": "Верховная Жрица", "suit": "Старшие Арканы", "meaning": "Интуиция, тайны, подсознание. Доверься внутреннему голосу."},
    {"name": "Императрица", "suit": "Старшие Арканы", "meaning": "Плодородие, творчество, изобилие. Заботься о себе."},
    {"name": "Император", "suit": "Старшие Арканы", "meaning": "Структура, порядок, дисциплина."},
    {"name": "Иерофант", "suit": "Старшие Арканы", "meaning": "Традиции, учитель, вера. Ищи наставника."},
    {"name": "Влюбленные", "suit": "Старшие Арканы", "meaning": "Любовь, выбор, гармония. Выбери сердцем."},
    {"name": "Колесница", "suit": "Старшие Арканы", "meaning": "Победа, контроль, движение. Не сдавайся!"},
    {"name": "Сила", "suit": "Старшие Арканы", "meaning": "Внутренняя сила, смелость, терпение."},
    {"name": "Отшельник", "suit": "Старшие Арканы", "meaning": "Мудрость, уединение, поиск."},
    {"name": "Колесо Фортуны", "suit": "Старшие Арканы", "meaning": "Судьба, перемена, удача."},
    {"name": "Справедливость", "suit": "Старшие Арканы", "meaning": "Честность, правда, равновесие."},
    {"name": "Повешенный", "suit": "Старшие Арканы", "meaning": "Жертва, переосмысление, отпускание."},
    {"name": "Смерть", "suit": "Старшие Арканы", "meaning": "Трансформация, конец и начало."},
    {"name": "Умеренность", "suit": "Старшие Арканы", "meaning": "Баланс, терпение, середина."},
    {"name": "Дьявол", "suit": "Старшие Арканы", "meaning": "Искушение, зависимость, разрушение."},
    {"name": "Башня", "suit": "Старшие Арканы", "meaning": "Крах, внезапное изменение, откровение."},
    {"name": "Звезда", "suit": "Старшие Арканы", "meaning": "Надежда, вдохновение, исцеление."},
    {"name": "Луна", "suit": "Старшие Арканы", "meaning": "Иллюзия, страх, интуиция."},
    {"name": "Солнце", "suit": "Старшие Арканы", "meaning": "Радость, успех, оптимизм."},
    {"name": "Суд", "suit": "Старшие Арканы", "meaning": "Пробуждение, перерождение, прощение."},
    {"name": "Мир", "suit": "Старшие Арканы", "meaning": "Завершение, целостность, удовлетворение."},
    {"name": "Туз Жезлов", "suit": "Жезлы", "meaning": "Вдохновение, энергия, начало."},
    {"name": "Двойка Жезлов", "suit": "Жезлы", "meaning": "Планирование, выбор, будущее."},
    {"name": "Тройка Жезлов", "suit": "Жезлы", "meaning": "Рост, расширение, уверенность."},
    {"name": "Четверка Жезлов", "suit": "Жезлы", "meaning": "Праздник, стабильность, дом."},
    {"name": "Пятерка Жезлов", "suit": "Жезлы", "meaning": "Конкуренция, конфликт, борьба."},
    {"name": "Шестерка Жезлов", "suit": "Жезлы", "meaning": "Победа, признание, успех."},
    {"name": "Семерка Жезлов", "suit": "Жезлы", "meaning": "Вызов, защита, стойкость."},
    {"name": "Восьмерка Жезлов", "suit": "Жезлы", "meaning": "Быстрота, перемены, энергия."},
    {"name": "Девятка Жезлов", "suit": "Жезлы", "meaning": "Стойкость, защита, готовность."},
    {"name": "Десятка Жезлов", "suit": "Жезлы", "meaning": "Бремя, ответственность, конец пути."},
    {"name": "Паж Жезлов", "suit": "Жезлы", "meaning": "Энтузиазм, новости, исследование."},
    {"name": "Рыцарь Жезлов", "suit": "Жезлы", "meaning": "Смелость, приключение, импульс."},
    {"name": "Королева Жезлов", "suit": "Жезлы", "meaning": "Теплота, уверенность, независимость."},
    {"name": "Король Жезлов", "suit": "Жезлы", "meaning": "Лидерство, сила, видение."},
    {"name": "Туз Кубков", "suit": "Кубки", "meaning": "Любовь, новые чувства, исцеление."},
    {"name": "Двойка Кубков", "suit": "Кубки", "meaning": "Союз, партнерство, взаимность."},
    {"name": "Тройка Кубков", "suit": "Кубки", "meaning": "Радость, дружба, праздник."},
    {"name": "Четверка Кубков", "suit": "Кубки", "meaning": "Апатия, разочарование, переоценка."},
    {"name": "Пятерка Кубков", "suit": "Кубки", "meaning": "Потеря, печаль, принятие."},
    {"name": "Шестерка Кубков", "suit": "Кубки", "meaning": "Ностальгия, детство, подарки."},
    {"name": "Семерка Кубков", "suit": "Кубки", "meaning": "Иллюзии, мечты, выбор."},
    {"name": "Восьмерка Кубков", "suit": "Кубки", "meaning": "Уход, перемены, исцеление."},
    {"name": "Девятка Кубков", "suit": "Кубки", "meaning": "Исполнение желаний, счастье."},
    {"name": "Десятка Кубков", "suit": "Кубки", "meaning": "Гармония, семья, вечная любовь."},
    {"name": "Паж Кубков", "suit": "Кубки", "meaning": "Нежность, новости, творчество."},
    {"name": "Рыцарь Кубков", "suit": "Кубки", "meaning": "Романтика, мечты, предложение."},
    {"name": "Королева Кубков", "suit": "Кубки", "meaning": "Интуиция, забота, мудрость."},
    {"name": "Король Кубков", "suit": "Кубки", "meaning": "Стабильность, доброта, мудрость."},
    {"name": "Туз Мечей", "suit": "Мечи", "meaning": "Ясность, прорыв, правда."},
    {"name": "Двойка Мечей", "suit": "Мечи", "meaning": "Трудный выбор, тупик, внутренний конфликт."},
    {"name": "Тройка Мечей", "suit": "Мечи", "meaning": "Боль, разрыв, освобождение."},
    {"name": "Четверка Мечей", "suit": "Мечи", "meaning": "Отдых, восстановление, спокойствие."},
    {"name": "Пятерка Мечей", "suit": "Мечи", "meaning": "Конфликт, победа ценой потерь."},
    {"name": "Шестерка Мечей", "suit": "Мечи", "meaning": "Переход, исцеление, движение вперед."},
    {"name": "Семерка Мечей", "suit": "Мечи", "meaning": "Хитрость, стратегия, скрытность."},
    {"name": "Восьмерка Мечей", "suit": "Мечи", "meaning": "Ограничения, страх, освобождение."},
    {"name": "Девятка Мечей", "suit": "Мечи", "meaning": "Тревога, кошмары, исцеление."},
    {"name": "Десятка Мечей", "suit": "Мечи", "meaning": "Конец, крах, новое начало."},
    {"name": "Паж Мечей", "suit": "Мечи", "meaning": "Бдительность, правда, ясность."},
    {"name": "Рыцарь Мечей", "suit": "Мечи", "meaning": "Скорость, прямота, конфликт."},
    {"name": "Королева Мечей", "suit": "Мечи", "meaning": "Честность, независимость, мудрость."},
    {"name": "Король Мечей", "suit": "Мечи", "meaning": "Власть, авторитет, логика."},
    {"name": "Туз Пентаклей", "suit": "Пентакли", "meaning": "Возможность, ресурсы, начало."},
    {"name": "Двойка Пентаклей", "suit": "Пентакли", "meaning": "Баланс, адаптация, управление."},
    {"name": "Тройка Пентаклей", "suit": "Пентакли", "meaning": "Успех, мастерство, сотрудничество."},
    {"name": "Четверка Пентаклей", "suit": "Пентакли", "meaning": "Стабильность, скупость, безопасность."},
    {"name": "Пятерка Пентаклей", "suit": "Пентакли", "meaning": "Трудности, бедность, испытание."},
    {"name": "Шестерка Пентаклей", "suit": "Пентакли", "meaning": "Щедрость, помощь, обмен."},
    {"name": "Семерка Пентаклей", "suit": "Пентакли", "meaning": "Ожидание, усилия, труд."},
    {"name": "Восьмерка Пентаклей", "suit": "Пентакли", "meaning": "Мастерство, детали, упорство."},
    {"name": "Девятка Пентаклей", "suit": "Пентакли", "meaning": "Достаток, комфорт, завершение."},
    {"name": "Десятка Пентаклей", "suit": "Пентакли", "meaning": "Наследие, стабильность, традиции."},
    {"name": "Паж Пентаклей", "suit": "Пентакли", "meaning": "Обучение, возможности, старт."},
    {"name": "Рыцарь Пентаклей", "suit": "Пентакли", "meaning": "Ответственность, работа, надежность."},
    {"name": "Королева Пентаклей", "suit": "Пентакли", "meaning": "Забота, практичность, плодородие."},
    {"name": "Король Пентаклей", "suit": "Пентакли", "meaning": "Богатство, успех, надежность."}
]

# ========== ФУНКЦИЯ ПОИСКА КАРТИНКИ ==========
card_numbers = {
    "Шут": "00", "Маг": "01", "Верховная Жрица": "02",
    "Императрица": "03", "Император": "04", "Иерофант": "05",
    "Влюбленные": "06", "Колесница": "07", "Сила": "08",
    "Отшельник": "09", "Колесо Фортуны": "10", "Справедливость": "11",
    "Повешенный": "12", "Смерть": "13", "Умеренность": "14",
    "Дьявол": "15", "Башня": "16", "Звезда": "17",
    "Луна": "18", "Солнце": "19", "Суд": "20", "Мир": "21",
    "Туз Жезлов": "22", "Двойка Жезлов": "23", "Тройка Жезлов": "24",
    "Четверка Жезлов": "25", "Пятерка Жезлов": "26", "Шестерка Жезлов": "27",
    "Семерка Жезлов": "28", "Восьмерка Жезлов": "29", "Девятка Жезлов": "30",
    "Десятка Жезлов": "31", "Паж Жезлов": "32", "Рыцарь Жезлов": "33",
    "Королева Жезлов": "34", "Король Жезлов": "35",
    "Туз Кубков": "36", "Двойка Кубков": "37", "Тройка Кубков": "38",
    "Четверка Кубков": "39", "Пятерка Кубков": "40", "Шестерка Кубков": "41",
    "Семерка Кубков": "42", "Восьмерка Кубков": "43", "Девятка Кубков": "44",
    "Десятка Кубков": "45", "Паж Кубков": "46", "Рыцарь Кубков": "47",
    "Королева Кубков": "48", "Король Кубков": "49",
    "Туз Мечей": "50", "Двойка Мечей": "51", "Тройка Мечей": "52",
    "Четверка Мечей": "53", "Пятерка Мечей": "54", "Шестерка Мечей": "55",
    "Семерка Мечей": "56", "Восьмерка Мечей": "57", "Девятка Мечей": "58",
    "Десятка Мечей": "59", "Паж Мечей": "60", "Рыцарь Мечей": "61",
    "Королева Мечей": "62", "Король Мечей": "63",
    "Туз Пентаклей": "64", "Двойка Пентаклей": "65", "Тройка Пентаклей": "66",
    "Четверка Пентаклей": "67", "Пятерка Пентаклей": "68", "Шестерка Пентаклей": "69",
    "Семерка Пентаклей": "70", "Восьмерка Пентаклей": "71", "Девятка Пентаклей": "72",
    "Десятка Пентаклей": "73", "Паж Пентаклей": "74", "Рыцарь Пентаклей": "75",
    "Королева Пентаклей": "76", "Король Пентаклей": "77"
}

def find_image(card_number):
    possible_paths = [
        f"images/{card_number}.jpg",
        f"images/{card_number}.jpeg",
        f"./{card_number}.jpg",
        f"./{card_number}.jpeg",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

# ========== КНОПКИ ==========
def get_main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("🔮 Карта дня", callback_data="card"),
        InlineKeyboardButton("📜 О Таро", callback_data="info"),
        InlineKeyboardButton("🆘 Помощь", callback_data="help"),
    ]
    keyboard.add(*buttons)
    return keyboard

def get_after_card_menu():
    keyboard = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton("🏠 В меню", callback_data="menu"),
    ]
    keyboard.add(*buttons)
    return keyboard

# ========== ГЛАВНАЯ ФУНКЦИЯ ОТПРАВКИ КАРТЫ ==========
def send_card(message, is_today=True):
    user_id = message.chat.id
    
    # Проверяем, есть ли у пользователя карта на сегодня
    user_card = get_user_card(user_id)
    
    if user_card:
        # Если карта уже есть — показываем её
        card_name, card_suit, card_meaning, card_number, date = user_card
        
        if is_today:
            response_text = (
                f"🌟 *Твоя карта дня уже ждала тебя!*\n\n"
                f"🃏 *{card_name}*\n"
                f"📜 *{card_suit}*\n\n"
                f"_{card_meaning}_\n\n"
                f"✨ Сегодня тебя ждёт именно это послание. Вернись к нему в течение дня."
            )
            
            image_path = find_image(card_number)
            if image_path:
                with open(image_path, 'rb') as photo:
                    bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=response_text,
                        parse_mode='Markdown',
                        reply_markup=get_after_card_menu()
                    )
            else:
                bot.send_message(
                    message.chat.id,
                    response_text,
                    parse_mode='Markdown',
                    reply_markup=get_after_card_menu()
                )
            return
    
    # Если карты нет — создаём новую
    card = random.choice(all_cards)
    card_number = card_numbers.get(card['name'], "00")
    
    # Сохраняем в базу
    save_user_card(user_id, card['name'], card['suit'], card['meaning'], card_number)
    
    response_text = (
        f"🌟 *Твоя карта дня:*\n\n"
        f"🃏 *{card['name']}*\n"
        f"📜 *{card['suit']}*\n\n"
        f"_{card['meaning']}_\n\n"
        f"✨ Сохрани это послание в своём сердце на сегодня."
    )
    
    image_path = find_image(card_number)
    if image_path:
        with open(image_path, 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=response_text,
                parse_mode='Markdown',
                reply_markup=get_after_card_menu()
            )
    else:
        bot.send_message(
            message.chat.id,
            response_text,
            parse_mode='Markdown',
            reply_markup=get_after_card_menu()
        )

# ========== КОМАНДЫ И КНОПКИ ==========

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🔮 *Приветствую, искатель мудрости!*\n\n"
        "Я твой личный оракул Таро. Каждый день я буду открывать тебе одну карту.\n\n"
        "✨ Нажми *«Карта дня»*, чтобы получить своё послание.\n"
        "Каждый пользователь получает уникальную карту, и она будет ждать тебя весь день."
    )
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

@bot.message_handler(commands=['card'])
def card_command(message):
    send_card(message, is_today=True)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.answer_callback_query(call.id)
    
    if call.data == "card":
        send_card(call.message, is_today=True)
    elif call.data == "info":
        send_info(call.message)
    elif call.data == "help":
        send_help(call.message)
    elif call.data == "menu":
        # Возвращаем главное меню (редактируем сообщение)
        try:
            bot.edit_message_text(
                "🔮 *Главное меню*\n\nВыбери действие:",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                parse_mode='Markdown',
                reply_markup=get_main_menu()
            )
        except Exception as e:
            # Если не получилось отредактировать — отправляем новое сообщение
            bot.send_message(
                call.message.chat.id,
                "🔮 *Главное меню*\n\nВыбери действие:",
                parse_mode='Markdown',
                reply_markup=get_main_menu()
            )
            print(f"Ошибка при редактировании: {e}")

def send_info(message):
    info_text = (
        "📜 *О картах Таро:*\n\n"
        "Таро — это древняя система символов, помогающая понять себя и мир вокруг.\n\n"
        "🃏 В моей колоде 78 карт:\n"
        "• 22 *Старших Аркана* — судьба и духовный путь\n"
        "• 56 *Младших Арканов* — повседневные события\n\n"
        "✨ Каждый день ты получаешь только одну карту. Доверься её мудрости."
    )
    try:
        bot.edit_message_text(
            info_text,
            message.chat.id,
            message.message_id,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
    except:
        bot.send_message(
            message.chat.id,
            info_text,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )

def send_help(message):
    help_text = (
        "🔮 *Доступные команды:*\n\n"
        "🔹 */start* — главное меню\n"
        "🔹 */card* — показать карту дня\n"
        "🔹 */info* — о Таро\n\n"
        "✨ Твоя карта дня уникальна и ждёт тебя ровно один день."
    )
    try:
        bot.edit_message_text(
            help_text,
            message.chat.id,
            message.message_id,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
    except:
        bot.send_message(
            message.chat.id,
            help_text,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(
        message.chat.id,
        "🌟 Нажми на кнопку в меню!",
        reply_markup=get_main_menu()
    )

# ========== ЗАПУСК ==========
print("🤖 Бот с ежедневными картами запущен!")
bot.infinity_polling()