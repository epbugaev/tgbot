import telebot
import datetime
import re

TOKEN = '5922991439:AAFtURg7fdlC0G1xPe-ZyTGAWi0BYTjXJ-o' # указываем токен нашего бота (для этого надо создать бота в @BotFather)

bot = telebot.TeleBot(TOKEN)


def check_access(message) -> bool:
    print(bot.get_chat_member(message.chat.id, message.from_user.id).status)
    return bot.get_chat_member(message.chat.id, message.from_user.id).status in ['owner', 'admin', 'creator', 'administrator']

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,"Hi, I am the most human bot (actually, some may argue I am not a bot at all!)")


@bot.message_handler(commands=['leave'])
def leave_chat(message):
    if check_access(message) == False:
        bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    bot.reply_to(message, "Okay I'll leave but think about what you've lost...")
    bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['help'])
def help(message):
    help_text = """
                Hi, my friend! List of commands:
                /help
                /start
                /leave
                /stat
                Everything below requires you to be admin:
                /ban (pass hours as argument)
                /unban
                /promote (new rights!!!)
                """
    bot.reply_to(message, help_text)


@bot.message_handler(content_types=['new_chat_members'])
def new_users(message):
    for user in message.new_chat_members:
        bot.send_message(message.chat.id, 'Hello?! Or goodbuy?(((')
        if datetime.datetime.now().second > 30:
            bot.send_message(message.chat.id, 'Now is not a good time, Ill call you later, by the way I know u r ' + user.first_name)
        else:
            bot.send_message(message.chat.id, 'What do you want master ' + user.username + '?')


@bot.message_handler(commands=['ban']) # Ban the user to whose message we reply
def ban(message):
    if check_access(message) == False:
        bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    numeric_arguments = re.findall(r'\d+(?=\s|$)', message.text)
    if len(numeric_arguments) > 1:
        bot.reply_to(message, 'Too many numeric arguments, I dont understand and feel sad :(' + str(numeric_arguments[0]))
        return

    if message.reply_to_message == None:
        bot.reply_to(message, 'Cannot ban user without their message, I cant track them :(')
        return

    victim_user = message.reply_to_message.from_user
    bot.ban_chat_member(message.chat.id, victim_user.id, until_date=datetime.datetime.now() + datetime.timedelta(hours=int(numeric_arguments[0])))


@bot.message_handler(commands=['unban'])
def unban(message):
    if check_access(message) == False:
        bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    if message.reply_to_message == None:
        bot.reply_to(message, 'Cannot unban user without their message, I cant track them :(')
        return
    victim_user = message.reply_to_message.from_user
    bot.unban_chat_member(message.chat.id, victim_user.id, only_if_banned=True)


@bot.message_handler(commands=['promote'])
def promote(message):
    if check_access(message) == False:
        bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    if message.reply_to_message == None:
        bot.reply_to(message, 'Cannot promote user without their message, I cant track them :(')
        return

    victim_user = message.reply_to_message.from_user
    bot.promote_chat_member(message.chat.id, victim_user.id,\
                                                              can_manage_chat=True,\
                                                              can_delete_messages=True,\
                                                              can_manage_video_chats=True,\
                                                              can_restrict_members=True,\
                                                              can_promote_members=True,\
                                                              can_change_info=True,\
                                                              can_invite_users=True,\
                                                              can_pin_messages=True)

    bot.reply_to(message, 'Promoted user ' + victim_user.username + '! Congratulations!')


@bot.message_handler(commands=['stat'])
def stat(message):
    admins_am = len(bot.get_chat_administrators(message.chat.id))
    users_am = bot.get_chat_member_count(message.chat.id)
    bot.reply_to(message, 'We have ' + str(users_am) + ' people total\n We have ' + str(admins_am) + ' people of power!\nSo exactly ' + str(users_am - admins_am) + ' are powerless!')


bot.polling(none_stop=True, interval=0) #запускаем нашего бота
