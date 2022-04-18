import logging
logging.basicConfig(level = logging.DEBUG,
                     format="%(asctime)s - %(name)s - %(message)s - %(levelname)s")

logger = logging.getLogger(__name__)

import pyrogram
import os

from config import BOT_TOKEN, APP_ID, API_HASH

logging.getLogger('pyrogram').setLevel(logging.WARNING)

if __name__ == '__main__':

    if not os.path.isdir('combo'):
        os.mkdir('combo')

    plugins = dict(root='plugins')

    app = pyrogram.Client(
        'Combo',
        bot_token=BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()