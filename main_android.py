'''
简介：Telegram Bot 程序，实现一个用来给用户看《三体》的Bot
创建时间：2022年4月28日
'''
from telegram import Update, ForceReply, ReplyKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackContext,MessageHandler,
    Filters,
)
import logging
import glob

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#读入三体
threeBody = open('三体.txt','rt',encoding='utf8').readlines()

#用户状态
user_pos = dict()


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_id = update.effective_user.id

    if user_id in user_pos:
        pass
    else:
        user_pos[user_id] = 0

    reply_keyboard = [['下一段']]
    update.message.reply_markdown_v2(
        fr'你好, {user.mention_markdown_v2()}, 点击发送 下一段 给我',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True
        ),)

def help(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['下一段']]
    update.message.reply_text('输入 ”下一段“ , 我读三体给你看 ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True
    ))

def next(update: Update, context: CallbackContext):
    '''
    发送下一段小说内容给用户
    '''
    user_id = update.effective_user.id
    reply_keyboard = [['下一段']]

    if user_id not in user_pos:
        user_pos[user_id] = 0

    pos = user_pos[user_id]
    if pos >= len(threeBody)-1:
        reply_text = '已完结'
    else:
        reply_text = threeBody[pos]

    update.message.reply_text(
          reply_text,
          reply_markup=ReplyKeyboardMarkup(
          reply_keyboard, resize_keyboard=True
          ),
    )
    #更新用户阅读位置
    user_pos[user_id]+=1


def save(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    with open(f'user_data/{user_id}.dat','wt',encoding='utf8') as user_data:
        print(f'写入{user_id}的数据')
        user_data.write(str(user_pos[user_id]))
    reply_keyboard = [['下一段']]
    update.message.reply_text('已保存阅读进度',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard, resize_keyboard=True
                              ))

def bot_restart():
    '''机器人重新开机'''
    for file in glob.glob('user_data/*.dat'):
        user_id = int(file.split('/')[1].split('.')[0])
        with open(file,'rt',encoding = 'utf8') as f:
            user_pos[user_id] = int(f.read())

def main() -> None:
    updater = Updater('5260554987:AAGbD2S8H81wzD-QQWavGUO_tEQdDszcU3k')

    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('下一段'), next))
    updater.dispatcher.add_handler(CommandHandler('save', save))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    bot_restart()
    main()
