import telebot

# 🔧 настройки
BOT_TOKEN = "7975395074:AAHB0LERhuhZerXPA1tqG5vHQSjBBl7vYUM"
ADMIN_ID = 7457494245  # без кавычек!

bot = telebot.TeleBot(BOT_TOKEN)

# сохраняем, кто кому пишет
user_to_admin = {}
admin_to_user = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "Привет! Напиши сюда своё сообщение, и админ его получит.")

@bot.message_handler(func=lambda m: True)
def forward_messages(msg):
    if msg.chat.id != ADMIN_ID:
        # обычный пользователь пишет админу
        text = f"📩 Сообщение от: {msg.from_user.first_name or '-'} (@{msg.from_user.username or '-'})\n\n{msg.text}"
        sent = bot.send_message(ADMIN_ID, text)
        user_to_admin[sent.message_id] = msg.chat.id
        admin_to_user[msg.chat.id] = sent.message_id
    else:
        # админ отвечает пользователю
        if msg.reply_to_message and msg.reply_to_message.message_id in user_to_admin:
            user_id = user_to_admin[msg.reply_to_message.message_id]
            bot.send_message(user_id, msg.text)
        else:
            bot.send_message(ADMIN_ID, "❗Ответь реплаем на сообщение пользователя.")

bot.infinity_polling()
