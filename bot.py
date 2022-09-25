"""
Простой бот для телеграмма
Сперва напишите функции обработки сообщений
Затем эти функции отправляются диспетчеру и регистрируются к соответствующим командам.
Затем бот запускается и работает пока вы не нажмёте Ctrl-C в консоли

Инструкция:
Просто эхо-бот.Повторяет сообщения
нажмите Ctrl-C консоли что бы остоновить бота
"""

#Библиотеки для бота
import logging #Пишет логи, очень полезная штука

#Делают за нас всю работу
from telegram import Update, ForceReply,InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler

import random

# Включаем логи
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text('Hi,'+ user.first_name+' !')
    #Продвинутый вариант
    # update.message.reply_markdown_v2(
    #     fr'Hi {user.mention_markdown_v2()}\!',
    #     reply_markup=ForceReply(selective=True),
    # )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('''/start - начало
/help - список комманд
/randomEmoji - случайная эмоция
/about - обо мне
/plus - сложение двух чисел
/divide - делит два числа
/quest - задает вопрос
/youtube - ссылка на ютуб
    ''')

def about_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Я ,великий и ужасный, создал этого бота в 2022 году!!!')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def randomEmoji(update: Update, context: CallbackContext) -> None:
    emojiList = ['😁','😂','😃','😄','😅','😍']
    myEmoji = random.choice(emojiList)
    update.message.reply_text(myEmoji)

# складываем два числа
def plus(update: Update, context: CallbackContext) -> None:
    try:
        one = int(context.args[0])
        two = int(context.args[1])
        answ = one+two
        update.message.reply_text(f"{one}+{two}={answ}")
    except (IndexError, ValueError):
        update.message.reply_text('Правильно: /plus <first_num> <second_num>')

# складываем два числа
def divide(update: Update, context: CallbackContext) -> None:
    try:
        one = int(context.args[0])
        two = int(context.args[1])
        if two == 0 :
            update.message.reply_text("На ноль делить нельзя!")
        else:
            answ = one/two
            update.message.reply_text(f"{one}/{two}={answ}")
    except (IndexError, ValueError):
        update.message.reply_text('Правильно: /divide <first_num> <second_num>')

def youtube(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('https://python-telegram-bot.org/')

def quest(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Камень", callback_data='Камень'),
            InlineKeyboardButton("Ножницы", callback_data='Ножницы'),
        ],
        [InlineKeyboardButton("Бумага", callback_data='Бумага')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Сделай выбор:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    answ = query.data
    wars = ["Камень", "Ножницы", "Бумага"]
    comp = random.choice(wars)
    if answ == comp:
        query.edit_message_text(text=f"{answ} i {comp} eto nichia")
    elif answ == "Камень" and comp == "Ножницы":
        query.edit_message_text(text=f"{answ} бьёт {comp}.Ты победил!")
    elif answ == "Ножницы" and comp == "Бумага":
        query.edit_message_text(text=f"{answ} бьёт {comp}.Ты победил!")
    elif answ == "Бумага" and comp == "Камень":
        query.edit_message_text(text=f"{answ} бьёт {comp}.Ты победил!")
    else:
        query.edit_message_text(text=f"{comp} бьёт {answ}.Ты проиграл!")

def main() -> None:
    """Запуск бота"""
    # Запускаем бота и передаём токен
    updater = Updater("5682288106:AAHbGxF-1_fqnGFfanmUULXOIVYmIoHmJDw")

    # Создаём диспечера
    dispatcher = updater.dispatcher

    # По разным командам запускаем разные функции
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("about", about_command))
    dispatcher.add_handler(CommandHandler("randomEmoji", randomEmoji))
    dispatcher.add_handler(CommandHandler("random", randomEmoji))
    dispatcher.add_handler(CommandHandler("youtube", youtube))

    # По разным командам запускаем разные функции
    updater.dispatcher.add_handler(CommandHandler('quest', quest))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_handler(CommandHandler("plus", plus))
    dispatcher.add_handler(CommandHandler("divide", divide))
    # По НЕ команде запускаем функцию эхо
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()