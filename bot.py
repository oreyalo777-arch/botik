import random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === НАСТРОЙКИ (ЗАМЕНИ ТОКЕН) ===
BOT_TOKEN = "8925535264:AAHqcSXI0AsZAeP6DayLcZ6k3T7Ll8tOQfc"

# === ТВОЙ СПИСОК ФРАЗ (замени на свои) ===
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
    "Сегодня я внимательно слушаю тебя и не перебиваю даже тогда, когда хочется", 
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
]

# === ВСТУПЛЕНИЕ (только один раз) ===
WELCOME_MESSAGE = (
    "Привет, Анечка, моя хорошая ❤️\n\n"
    "Я - бот, который создан, чтобы напоминать тебе о самом главном. "
    "Каждый день я буду дарить тебе одну фразу, их можно переносить и накапливать)"
    "Она будет о тебе и для тебя.\n\n"
    "Просто напиши /bublik, и я скажу тебе то, что хочу говорить тебе каждый день.\n\n"
    "Я очень люблю тебя!! Твоя Дианочка🥺❤️"
)

# === ХРАНИЛИЩА (не трогать) ===
used_phrases = []
last_used_date = {}  # теперь храним ДЕНЬ, когда была получена фраза
welcomed_users = set()

# === ЛОГИКА БОТА ===
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global used_phrases
    user_id = update.effective_user.id
    today = datetime.now().date()  # получаем сегодняшнюю дату (без времени)

    # Вступление (один раз)
    if user_id not in welcomed_users:
        welcomed_users.add(user_id)
        await update.message.reply_text(WELCOME_MESSAGE)

    # Проверка, получала ли она фразу СЕГОДНЯ
    if user_id in last_used_date and last_used_date[user_id] == today:
        await update.message.reply_text(
            "🌙 Ты уже получила свою фразу сегодня. Приходи завтра, после полуночи ❤️"
        )
        return

    # Выбор фразы
    available = [p for p in PHRASES if p not in used_phrases]
    if not available:
        used_phrases = []
        available = PHRASES[:]
    
    chosen = random.choice(available)
    used_phrases.append(chosen)
    last_used_date[user_id] = today  # запоминаем, что сегодня уже выдано
    await update.message.reply_text(chosen)

# === ЗАПУСК ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", handle))
    app.add_handler(CommandHandler("bublik", handle))  # изменено на /bublik
    print("✅ Бот запущен! Фразы выдаются раз в календарный день.")
    app.run_polling()

if __name__ == "__main__":
    main()