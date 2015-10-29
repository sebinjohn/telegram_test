from twx.botapi import TelegramBot

with open('.tokenfile') as inf:
    API_TOKEN = inf.readline().split('=')[1]

print API_TOKEN
bot = TelegramBot(API_TOKEN)
print(bot.update_bot_info().wait())
print(bot)
print "I am a bot : " + str(bot.username)

what_i_can_do = ['/start', '/size']

initial_offset = 0
offsets = []
while offsets == []:
    updates = bot.get_updates(offset=initial_offset).wait()
    for update in updates:
        offsets.append(update.update_id)

chat_start_offset = max(offsets) + 1


def reply_to_chat(bot, chat_id, with_message=''):
    result = bot.send_message(chat_id, with_message).wait()
    return result

def get_dir_size(hdfs_dir):
    with open('size.csv') as inf:
        for line in inf:
            if line.startwith(hdfs_dir + ','):
                return line.split(',')[1]
    return None

while True:
    updates = bot.get_updates(offset=chat_start_offset).wait()
    for update in updates:
        what_i_got = update.message.text
        chat_id = update.message.chat.id
        if what_i_got.startswith('@'):
            what_i_should_do = what_i_got.split(' ')[1:]
        else:
            what_i_should_do = what_i_got.split('')

        if what_i_should_do not in what_i_can_do:
            reply_to_chat(bot, chat_id, "I am sorry, I can't understand it. But, What I can do is " + str(what_i_can_do))
        elif what_i_should_do[0] == '/start':
            reply_to_chat(bot, chat_id, "Hi, I am ready :)")
        elif what_i_should_do[0] == '/size':
            hdfs_dir = what_i_should_do[1]
            size = get_dir_size(hdfs_dir)
            if size:
                reply_to_chat(bot, chat_id, size)
            else:
                reply_to_chat(bot, chat_id, "Today's data is not available")
