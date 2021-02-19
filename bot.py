import config
import youtube_dl
import os
import telebot

bot = telebot.TeleBot(config.Token)

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('src/welcome_sti.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)
	bot.send_message(message.chat.id, 'Здраствуйте ' + str(message.from_user.first_name) + '!\nДля скачивания видоса напишите - /download\nДля получения помощи напишите - /help')

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.chat.id,'\nДля скачивания видоса в формате mp4 напишите - /download <link>\nДля скачивания ТОЛЬКО аудио дорожки в формате mp3 напишите - /downloadmp3 <link>')

@bot.message_handler(commands=['download'])
def dowload(message):
	msg = message.text.split()
	if len(msg) != 2:
		bot.send_message(message.chat.id,"Вы неправильно ввели команду, правильный ввод: /download <link>")
	else:
		bot.send_message(message.chat.id,"Пожалуйста, подождите, это может занять несколько минут...")
		link = msg[1]
		ydl_opts = {
			'format': 'best',
			'postprocessors': [{
				'key': 'FFmpegVideoConvertor',
        		'preferedformat': 'mp4',
			}],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])

		for file in os.listdir("./"):
			if file.endswith(".mp4"):
				os.rename(file, "video.mp4")

		bot.send_document(message.chat.id, open(r'video.mp4', 'rb'))
		os.remove("video.mp4")

@bot.message_handler(commands=['downloadmp3'])
def dowload(message):
	msg = message.text.split()
	if len(msg) != 2:
		bot.send_message(message.chat.id,"Вы неправильно ввели команду, правильный ввод: /downloadmp3 <link>")
	else:
		bot.send_message(message.chat.id,"Пожалуйста, подождите, это может занять несколько минут...")
		link = msg[1]
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192',
			}],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([link])

		for file in os.listdir("./"):
			if file.endswith(".mp3"):
				os.rename(file, "song.mp3")

		bot.send_document(message.chat.id, open(r'song.mp3', 'rb'))
		os.remove("song.mp3")

bot.polling(none_stop=True)
