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

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

#读入三体
threeBody = open('测试三体.txt','rt',encoding='utf8').readlines()

#用户状态
user_pos = dict()


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_id = update.effective_user.id
    user_pos[user_id]=0
    reply_keyboard = [['下一段']]
    update.message.reply_markdown_v2(
        fr'你好, {user.mention_markdown_v2()}, 来读《三体》吧,点击发送 下一段 给我',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),)

def help(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['下一段']]
    update.message.reply_text('输入 ”下一段“ , 我读三体给你看 ',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
    ))

def next(update: Update, context: CallbackContext):
    '''
    发送下一段小说内容给用户
    '''
    user_id = update.effective_user.id
    reply_keyboard = [['下一段']]

    pos = user_pos[user_id]
    if pos >= len(threeBody)-1:
        reply_text = '已完结'
    else:
        reply_text = threeBody[pos]

    update.message.reply_text(
          reply_text,
          reply_markup=ReplyKeyboardMarkup(
          reply_keyboard, one_time_keyboard=True
          ),
    )
    #更新用户阅读位置
    user_pos[user_id]+=1


def main() -> None:
    updater = Updater('5260554987:AAGbD2S8H81wzD-QQWavGUO_tEQdDszcU3k')

    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text('下一段'), next))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()