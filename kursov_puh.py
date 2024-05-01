import telebot
from g4f.client import Client

TOKEN = '6531296471:AAER0UQexHqI0xerJLs2Qe_b7tImRUqnYSM'
bot = telebot.TeleBot(TOKEN)

processing = False
mode = "обычный"
prompt = ""

def create_keyboard():
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2)
    btn1 = telebot.types.InlineKeyboardButton(text="Научный режим", callback_data="научный")
    btn2 = telebot.types.InlineKeyboardButton(text="Обычный режим", callback_data="обычный")
    keyboard.add(btn1, btn2)
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Выберите режим:", reply_markup=create_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global mode, prompt
    if call.data == "научный":
        mode = "научный"
        prompt = "напиши статью в научном стиле по ключевым словам: "
        bot.send_message(call.message.chat.id, "Вы выбрали научный режим. Напишите ключевые слова")
    elif call.data == "обычный":
        mode = "обычный"
        prompt = "напиши историю по ключевым словам: "
        bot.send_message(call.message.chat.id, "Вы выбрали обычный режим. Продолжаем")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global processing, prompt

    if processing:
        bot.reply_to(message, "Подождите, пока не завершится предыдущий запрос")
    else:
        processing = True

        keywords = message.text
        responsing = prompt + keywords
        client = Client()
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": responsing}])
        sendme = response.choices[0].message.content
        
        bot.reply_to(message, sendme) 
        processing = False

bot.polling(none_stop=True)
