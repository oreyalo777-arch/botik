import random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
import threading

# === НАСТРОЙКИ ===
BOT_TOKEN = "8925535264:AAHqcSXI0AsZAeP6DayLcZ6k3T7Ll8tOQfc"

# === ТВОЙ СПИСОК ФРАЗ ===
PHRASES = [
    "Я готовлю или заказываю сегодня всё, что ты хочешь❤️",
    "Милая, я очень сильно люблю тебя, сегодня давишь мне сколько угодно прыщей и я не пищу)",
    "Анечка, сегодня выполняю всё, что ты попросишь, но желание у тебя одно❤️",
    "Солнышко, ты сегодня невероятно красива, как и всегда, моя прелесть!!🥺",
    "Дарю тебе массаж, жди вечером)",
    "Сегодня готова сделать за тебя всё, что ты попросишь❤️🫂",
    "Сегодня вечером делаем всё, что хочешь ты!",
    "Купон на обнимашки, а ну иди сюда моя прелесть😈😈😈",
    "Купон на прогулку туда, куда ты хочешь)", 
    "Купон на ванну с шиммером и бомбочкой и поцелуи в носик!!",
    "Купон на ответ на любой твой вопрос)",
    "Я доначу тебе в ферму))",
    "Купон на совместную игру в ферму",
    "Я очень люблю тебя всегда, даже когда тебе кажется, что это не так🫂",
    "Я внимательно слушаю тебя и не перебиваю даже тогда, когда хочется", 
    "Купон на парную йогу🤯",
    "Тебе очень идет розовый, малыш)",
    "Не забывай пить воду, милая!!",
    "Сегодня смотрим только то, что ты выберешь",
    "Купон на рисование вместе", 
    "Мы идем в театр, побежали выбирать постановку!!",
    "Мы идем на концерт, выбирай исполнителя!!",
    "Купон на мытую посуду)",
    "Ты самая прекрасная девочка на свете!!",
    "Анечка, ты моя прелесть, целую в носик!!",
    "Купон на поход в музей)",
    "Купон на поход на каток",
    "Сегодня я гуляю с Тошей, если хочешь)",
    "Я покупаю тебе любую штучку, которую ты попросишь)",
    "Купон на вкусный тортик",
    "Готовим вместе что нибудь вкусненькое",
    "Обнимаю тебя и глажу столько, сколько ты захочешь!",
    "Ты очень милая, бублик, обнимаю🥺",
]

# === ВСТУПЛЕНИЕ ===
WELCOME_MESSAGE = (
    "Привет, Анечка, моя хорошая ❤️\n\n"
    "Я - бот, который создан, чтобы напоминать тебе о самом главном. "
    "Каждый день я буду дарить тебе одну фразу, их можно переносить и накапливать)"
    "Она будет о тебе и для тебя.\n\n"
    "Просто напиши /bublik, и я скажу тебе то, что хочу говорить тебе каждый день.\n\n"
    "Я очень люблю тебя!! Твоя Дианочка🥺❤️"
)

# === ХРАНИЛИЩА ===
used_phrases = []
last_used_date = {}
welcomed_users = set()

# === ЛОГИКА БОТА ===
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global used_phrases
    user_id = update.effective_user.id
    today = datetime.now().date()

    # Вступление (один раз) — ТОЛЬКО вступление, без фразы
    if user_id not in welcomed_users:
        welcomed_users.add(user_id)
        await update.message.reply_text(WELCOME_MESSAGE)
        return  # Выходим, чтобы не выдавать фразу

    # Проверка на сегодняшнюю фразу
    if user_id in last_used_date and last_used_date[user_id] == today:
        await update.message.reply_text("🌙 Ты уже получила свою фразу сегодня. Приходи завтра ❤️")
        return

    # Выбор фразы
    available = [p for p in PHRASES if p not in used_phrases]
    if not available:
        used_phrases = []
        available = PHRASES[:]

    chosen = random.choice(available)
    used_phrases.append(chosen)
    last_used_date[user_id] = today
    await update.message.reply_text(chosen)

async def reset_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сбрасывает историю для пользователя, который вызвал команду"""
    user_id = update.effective_user.id

    if user_id in welcomed_users:
        welcomed_users.remove(user_id)
    if user_id in last_used_date:
        del last_used_date[user_id]

    await update.message.reply_text("✅ Твоя история сброшена ❤️")

# === ВЕБ-СЕРВЕР ДЛЯ RENDER ===
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    return "Бот работает!", 200

def run_web_server():
    flask_app.run(host='0.0.0.0', port=10000)

# === ЗАПУСК ===
def main():
    # Запускаем веб-сервер в отдельном потоке
    thread = threading.Thread(target=run_web_server, daemon=True)
    thread.start()

    # Запускаем Telegram-бота
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", handle))
    app.add_handler(CommandHandler("bublik", handle))
    app.add_handler(CommandHandler("reset_me", reset_user))
    print("✅ Бот запущен! Веб-сервер тоже работает.")
    app.run_polling()

if __name__ == "__main__":
    main()
