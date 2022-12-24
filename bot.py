from telebot.async_telebot import AsyncTeleBot, types
import asyncio
import aioschedule
import datetime
import re

TOKEN = '' # указываем токен нашего бота (для этого надо создать бота в @BotFather)

bot = AsyncTeleBot(TOKEN)

async def check_access(message) -> bool:
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ['owner', 'admin', 'creator', 'administrator']

@bot.message_handler(commands=['start'])
async def welcome(message):
    await bot.send_message(message.chat.id,"Hi, I am the most human bot (actually, some may argue I am not a bot at all!)")


@bot.message_handler(commands=['leave'])
async def leave_chat(message):
    if await check_access(message) == False:
        await bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    await bot.reply_to(message, "Okay I'll leave but think about what you've lost...")
    await bot.leave_chat(message.chat.id)


@bot.message_handler(commands=['help'])
async def help(message):
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
    await bot.reply_to(message, help_text)


@bot.message_handler(content_types=['new_chat_members'])
async def new_users(message):
    for user in message.new_chat_members:
        await bot.send_message(message.chat.id, 'Hello?! Or goodbuy?(((')
        if datetime.datetime.now().second > 30:
            await bot.send_message(message.chat.id, 'Now is not a good time, Ill call you later, by the way I know u r ' + user.first_name)
        else:
            await bot.send_message(message.chat.id, 'What do you want master ' + user.username + '?')


@bot.message_handler(commands=['ban']) # Ban the user to whose message we reply
async def ban(message):
    if await check_access(message) == False:
        await bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    numeric_arguments = re.findall(r'\d+(?=\s|$)', message.text)
    if len(numeric_arguments) > 1 or len(numeric_arguments) == 0:
        await bot.reply_to(message, 'Too many numeric arguments, I dont understand and feel sad :(' + str(numeric_arguments[0]))
        return  

    if message.reply_to_message == None:
        await bot.reply_to(message, 'Cannot ban user without their message, I cant track them :(')
        return

    victim_user = message.reply_to_message.from_user
    await bot.ban_chat_member(message.chat.id, victim_user.id, until_date=datetime.datetime.now() + datetime.timedelta(hours=int(numeric_arguments[0])))


@bot.message_handler(commands=['unban'])
async def unban(message):
    if await check_access(message) == False:
        await bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    if message.reply_to_message == None:
        await bot.reply_to(message, 'Cannot unban user without their message, I cant track them :(')
        return
    victim_user = message.reply_to_message.from_user
    await bot.unban_chat_member(message.chat.id, victim_user.id, only_if_banned=True)


@bot.message_handler(commands=['promote'])
async def promote(message):
    if await check_access(message) == False:
        await bot.reply_to(message, 'You dont have the power to command me, I refuse to work.')
        return

    if message.reply_to_message == None:
        await bot.reply_to(message, 'Cannot promote user without their message, I cant track them :(')
        return

    victim_user = message.reply_to_message.from_user
    await bot.promote_chat_member(message.chat.id, victim_user.id,\
                                                              can_manage_chat=True,\
                                                              can_delete_messages=True,\
                                                              can_manage_video_chats=True,\
                                                              can_restrict_members=True,\
                                                              can_promote_members=True,\
                                                              can_change_info=True,\
                                                              can_invite_users=True,\
                                                              can_pin_messages=True)

    await bot.reply_to(message, 'Promoted user ' + victim_user.username + '! Congratulations!')


@bot.message_handler(commands=['stat'])
async def stat(message):
    admins_am = len(await bot.get_chat_administrators(message.chat.id))
    users_am = await bot.get_chat_member_count(message.chat.id)
    await bot.reply_to(message, 'We have ' + str(users_am) + ' people total\n We have ' + str(admins_am) + ' people of power!\nSo exactly ' + str(users_am - admins_am) + ' are powerless!')


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())

asyncio.run(main())
