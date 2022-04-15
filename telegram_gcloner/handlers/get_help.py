#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

from telegram.ext import Dispatcher, CommandHandler

from utils.config_loader import config
from utils.callback import callback_delete_message
from utils.restricted import restricted

logger = logging.getLogger(__name__)


def init(dispatcher: Dispatcher):
    """Provide handlers initialization."""
    dispatcher.add_handler(CommandHandler('help', get_help))


@restricted
def get_help(update, context):
    message = 'Google Drive linkini gönderin, veya Google drive linki olan bir dosyayı elle transfer için iletin.\n' \
              'Yapılandırmak için /sa ve /folders komutları gereklidir.\n\n' \
              '📚 Komutlar:\n' \
              ' │ /start - Botu başlatır.' \
              ' │ /folders - favori klasörü seçer.' \
              ' │ /sa - Sadece direkt mesajda. İçinde Servis hesapları olan dosyayı seçmenize olanak sağlar.\n' \
              ' │ /ban - Bir kişi, bu botu kullanmaktan men eder.' \
              ' │ /unban - Men edilmiş kullanıcının bota erişmesine tekrar izin verilir.' \
              ' │ /id - Kullanıcı ID\'ni verir.' \
              ' │ /contact - Botun sahibine mesaj gönderir.' \
              ' │ /help - Bu mesajı gönderir.\n'

    rsp = update.message.reply_text(message)
    rsp.done.wait(timeout=60)
    message_id = rsp.result().message_id
    if update.message.chat_id < 0:
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, message_id))
        context.job_queue.run_once(callback_delete_message, config.TIMER_TO_DELETE_MESSAGE,
                                   context=(update.message.chat_id, update.message.message_id))
