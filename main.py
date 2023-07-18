# Импорты для дополнительного задания
import os.path
import subprocess
import speech_recognition as sr
import requests
import telebot.types

# Основной бот
from telebot import TeleBot, types

import config

bot = TeleBot(config.BOT_TOKEN)
bot.set_my_commands([
    types.BotCommand("/aboutauthor", "Информация об авторе"),
    types.BotCommand("/aboutbot", "Информация о боте"),
    types.BotCommand("/github", "Получить ссылку на репозиторий"),
    types.BotCommand("/help", "Доступные команды"),
    types.BotCommand("/photo", "Получить фото автора"),
    types.BotCommand("/nextstep", "Доступные команды"),
    types.BotCommand("/start", "Запуск бота"),
    types.BotCommand("/voice", "Услышать рассказ автора на одну из 3 тем"),
])


@bot.message_handler(commands=["start"])
def start_bot(message):
    bot.send_message(message.from_user.id, "Добро пожаловать в тестовый бот наставника kids ai!")


@bot.message_handler(commands=["help", "nextstep"])
def get_next_step(message):
    bot.send_message(message.from_user.id, "Данный бот понимает следующие команды:\n\n"
                                           "/aboutauthor информация о создателе бота\n"
                                           "/aboutbot информация о боте\n"
                                           "/github ссылка на репозиторий\n"
                                           "/help список команд бота\n"
                                           "/photo посмотреть последнее селфи или школьное фото создателя бота\n"
                                           "/nextstep - доступные команды\n"
                                           "/start начало работы\n"
                                           "/voice получить войс создателя бота на одну из трех тем.\n"
                                           "Также этот бот умеет распознавать голосовые команды (по-русски)!")


@bot.message_handler(commands=["aboutbot"])
def get_info_about_bot(message: types.Message):
    bot.send_message(message.from_user.id, "Данный бот создан программистом Андреем Фроловым "
                                           "в процессе выполнения тестового задания от Яндекс.Практикума "
                                           "для наставничества в программе Kids AI. "
                                           "Бот отвечает следующим требованиям: распознает команды, "
                                           "имеет reply- и inline-кнопки, а также умеет присылать фотографии, "
                                           "отправлять и получать голосовые сообщения в рамках поставленных задач.")


@bot.message_handler(commands=["aboutauthor"])
def get_info_about_author(message: telebot.types.Message):
    # bot.send_message(message.from_user.id, "Бла бла бла информация обо мне. НИКА, ПОМОГИ, ПОЖАЛУЙСТА")
    markup = types.InlineKeyboardMarkup()
    btn_hh_site = types.InlineKeyboardButton(text='Моё резюме',
                                             url='https://hh.ru/resume/faaa3fbdff0c0219ec0039ed1f733749553875')
    markup.add(btn_hh_site)
    bot.send_message(message.chat.id, "Здравствуйте! Меня зовут Андрей Фролов, я работаю C++ разработчиком "
                                      "в инжиниринговой компании Тесис. Мне 27, я люблю заниматься спортом "
                                      "и активно проводить время. Вы можете более подробно ознакомиться "
                                      "с моим опытом работы, перейдя по ссылке.", reply_markup=markup)


@bot.message_handler(commands=["github"])
def get_source_code(message: types.Message):
    # todo: Выложить на гитхаб
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='Репозиторий',
                                             url='https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Ссылка на репозиторий с кодом проекта", reply_markup=markup)


@bot.message_handler(commands=["voice"])
def get_voice(message: telebot.types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn_GPT = types.InlineKeyboardButton(text="Про GPT для бабушки", callback_data="btn_GPT")
    btn_BD = types.InlineKeyboardButton(text="Отличия SQL от No-SQL", callback_data="btn_BD")
    btn_LOVE = types.InlineKeyboardButton(text="История первой любви", callback_data="btn_LOVE")
    keyboard.add(btn_GPT, btn_BD, btn_LOVE)
    bot.send_message(message.chat.id, "Выберите интересующую тему", reply_markup=keyboard)


@bot.message_handler(commands=["photo"])
def get_photo(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    btn_now = types.KeyboardButton(text="Свежее селфи")
    btn_school = types.KeyboardButton(text="Школьное фото")
    keyboard.add(btn_now, btn_school)
    bot.send_message(message.chat.id, "Выберите фото", reply_markup=keyboard)
    bot.register_next_step_handler(message, process_photo_step)


def process_photo_step(message: types.Message):
    try:
        if message.text == "Свежее селфи":
            with open(r"res/Свежее селфи.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "Школьное фото":
            with open(r"res/Школьное фото.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, "У меня нет таких фотографий", reply_markup=types.ReplyKeyboardRemove())
    except Exception:
        bot.reply_to(message, "Произошла внутренняя ошибка. Надеюсь, ничего не сломалось)",
                     reply_markup=types.ReplyKeyboardRemove())


@bot.callback_query_handler(func=lambda callback: callback.data)
def process_callback(callback: types.CallbackQuery):
    match callback.data:
        case "btn_GPT":
            with open(r'res/Про GPT.ogg', 'rb') as audio:
                bot.send_audio(callback.message.chat.id, audio)
        case "btn_BD":
            with open(r'res/Про базы данных.ogg', 'rb') as audio:
                bot.send_audio(callback.message.chat.id, audio)
        case "btn_LOVE":
            with open(r'res/Про первую любовь.ogg', 'rb') as audio:
                bot.send_audio(callback.message.chat.id, audio)


@bot.message_handler(content_types=["voice"])
def process_voice_command(message: types.Message):
    file_oga = None
    file_wav = None
    try:
        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        file_oga = os.path.basename(file_path)
        file_wav = os.path.splitext(file_oga)[0] + ".wav"
        saved_file = requests.get(f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_path}")
        with open(file_oga, "wb") as file:
            file.write(saved_file.content)
        subprocess.run(['ffmpeg/ffmpeg.exe', '-i', file_oga, file_wav])
        result = voice_to_text(file_wav)
        if result in config.VOICE_COMMANDS:
            bot.send_message(message.chat.id, f"Распознана команда {config.VOICE_COMMANDS[result]}")
            match result:
                case "старт":
                    start_bot(message)
                case "помощь":
                    get_next_step(message)
                case "об авторе":
                    get_info_about_author(message)
                case "о боте":
                    get_info_about_bot(message)
                case "гитхаб":
                    get_source_code(message)
                case "голос":
                    get_voice(message)
                case "фото":
                    get_photo(message)
        else:
            bot.send_message(message.chat.id, f"Распознан текст \"{result}\"")
    except sr.UnknownValueError:
        bot.send_message(message.chat.id, "Не удалось распознать голосовую команду")
    except Exception:
        bot.send_message(message.chat.id, "Произошла внутренняя ошибка. Надеюсь, ничего не сломалось)")
    finally:
        # В любом случае удаляем временные файлы с аудио сообщением
        if file_oga:
            os.remove(file_oga)
        if file_wav:
            os.remove(file_wav)
    print(message)


def voice_to_text(file_name: str):
    recognizer = sr.Recognizer()
    message_text = sr.AudioFile(file_name)
    with message_text as source:
        voice = recognizer.record(source)
    return recognizer.recognize_google(voice, language="ru_RU")


if __name__ == "__main__":
    bot.polling()
