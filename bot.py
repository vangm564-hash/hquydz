import telebot
import threading
import time
import random
import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask

# --- HỆ THỐNG DUY TRÌ ---
app = Flask(__name__)
@app.route('/')
def home(): return "SYSTEM ONLINE"

# --- DATABASE ---
DATA_FILE = "bot_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    return {"admins": [7153197678], "keys": {}, "authorized_groups": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_data()
OWNER_ID = 7153197678
DELAY_TIME = 0.1
stop_event = threading.Event()
BLACKLIST = {}

# --- NẠP 29 TOKEN ---
RAW_TOKENS = [
    '8675065386:AAHVtY8NYQOykrCCEQ9tQDpe_mZK9XUmVV0', '8750639984:AAGAU7SsEe_V9CpZ9LAfxovI2iFWSCQ9riw',
    '8423233437:AAFPeFNFctZlgO8VU_KGkp_HT71FCTywUmI', '8705345450:AAHAxsFUHu7ux4USLvItL018KD4hBsTe4_Q',
    '8144155270:AAH-y47kIAFWgo7sge1VmCMrx2dc9CkYxOs', '8688293059:AAGoga_q3E7VbZQ3sL6xZ3-vzGgtC7RsTmc',
    '8652311818:AAGmFWSeRYW1-RQ-RH8jNguwkRtzFt0U-oQ', '8731497895:AAHHhCiAp7a62eflQBe0PztWw0jRjDPpyk4',
    '8684330434:AAEORwA4uvBXIm-orys4txSttOnkH2CRwZ4', '8796842934:AAENmEMod5CHQxfcl6Z5kl3nlwv8slQLJJc',
    '8668865669:AAGMgG3zBSN69eDYzTHENxl6Y9AAj6Kln4Q', '8429960682:AAHltNvwWjEn1QC_f5R8JPgz7uN1uFhny18', 
    '8481938728:AAGen1t8Tz3jeu02kJ8HoCIZLiPLdd687n8', '8739448460:AAGNLEW-WDvatvatMplzkziG5pd5hTRfqiE', 
    '8689807630:AAEoXvm45QaW1jlT-H_KzNlmCpu50Q3k2S4', '8575475228:AAHRtsOcCEQInRvR3isSBV-Igur-WykB_PE', 
    '8651553692:AAGNQwqUoWgV1QV0ozaZHLRL0RJm9M8q0e0', '8712129360:AAEgW2hBbtsgY8DyMd9mxYw1B6X8_VBpF-g', 
    '8626439785:AAEn2pArlYu0KW9tHLETtrJUXKo2BR0hjx0', '8793582382:AAHfbcee8kt-x6OeLHqwqXP79U4PBaII0MA', 
    '8397463503:AAGajcEI5H_SJ0i6mccvPT7GC-P8U5RTLOQ', '8718672219:AAH37zxnCBuWLMSEW_rCvEwnrf0ym8d7-H0', 
    '8650032681:AAE9TeiIIywG796f6hHLN7JiBWhNgH3gc', '8303481123:AAFN_bijtWzXlR1FlYHEvgN-5uhyqnZsbu0', 
    '8619086108:AAFYqRAdKNvg84eyj1ylXfa-TF8W8o8fxbo', '8661308767:AAFU__yZv8r1HlJ5jaW3URW88bWKWYKDCCY', 
    '8625550674:AAHIHuakDCvvxwCC0mgrDLU5g8vBNFdD7eI', '8724848112:AAHhLYnH1LO4tVUPMTjztbNZZtni7D0uDl4', 
    '8471422557:AAF30BcMF15veQPHCTDqcA1NU0iHb63Zm1o'
]
VALID_BOTS = []

# --- XỬ LÝ NGÔN CHỬI (CHIA ĐỀU MỖI CÂU 1 DÒNG) ---
def get_ngon_tu():
    all_lines = []
    for fname in ["ngontagtele.txt", "chui.txt"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as f:
                            for line in f:
                clean = line.strip()
                if clean and not clean.startswith("["):
                    all_lines.append(clean)

    chunk = len(all_lines) // 4)
    return {
        "sp": all_lines[:chunk],
        "sp2": all_lines[chunk:chunk*2],
        "sptag": all_lines[chunk*2:chunk*3],
        "spslow": all_lines[chunk*3:]
    }

KHO_DAN = get_ngon_tu()

def is_admin(uid): return uid in db["admins"] or uid == OWNER_ID

# --- THREAD TẤN CÔNG ---
def attack_logic(bot, chat_id, lines, mode="normal"):
    while not stop_event.is_set():
        msg = random.choice(lines)
        try:
            bot.send_message(chat_id, msg)
            time.sleep(DELAY_TIME if mode == "normal" else 2.5)
        except: break

def start_master():
    if not VALID_BOTS: return
    master = VALID_BOTS[0]

    @master.message_handler(func=lambda m: True)
    def handle_all(m):
        global DELAY_TIME, stop_event, BLACKLIST
        uid = m.from_user.id
        args = m.text.split()
        if not args: return
        cmd = args[0].lower()

        # Tự xóa tin nhắn (Câm mõm)
        if m.chat.id in BLACKLIST and uid in BLACKLIST[m.chat.id]:
            try: master.delete_message(m.chat.id, m.message_id)
            except: pass
            return

        # MENU CHÍNH
        if cmd == '/help':
            master.reply_to(m, (
                ". 　˚　. . ✦˚ .     　　˚　　　　✦　.\n"
                "𖣘 Hai Quy.   2026 𖣘\n"
                ".  ˚　.　 . ✦　˚　 .   .　.  　˚　  　.\n\n"
                "🔥 𝑺𝒑𝒂𝒎 & 𝑻𝒂𝒈\n"
                "┣ /sp - Spam\n"
                "┣ /sp2 - Spam\n"
                "┣ /spnd <nd> - Spam nội dung \n"
                "┣ /sptag - Tag ẩn\n"
                "┗ /spslow - spam cham\n\n"
                "☠ 𝑯𝒆‌‌ 𝑻𝒉𝒐‌‌𝒏𝒈 Deo Ro‌‌\n"
                "┣ /cam - đeo rọ\n"
                "┣ /sua - cho sủa\n"
                "┣ /clear - Xoa tin nhan spam\n"
                "┣ /listbot - Check bot\n"
                "┗ /setdelay - Chỉnh tốc độ SPAM\n\n"
                "📦 𝑳𝒂‌𝒕 𝑽𝒂‌𝒕\n"
                "┣ /dung - Dừng spam \n"
                "┣ /setkey - Nhập mã Key\n"
                "┗ /info - Soi ID\n"
                "👤 ADMIN: Hquy"
            ))

        # LỆNH /DUNG (DỪNG TẤT CẢ)
        elif cmd == '/dung':
            stop_event.set()
            master.reply_to(m, "🛑 **STOP!**")

        # LOGIC SPAM
        if cmd in ['/sp', '/sp2', '/sptag', '/spslow']:
            stop_event.clear()
            key = cmd[1:]
            dan = KHO_DAN.get(key, KHO_DAN['sp'])
            mode = "slow" if cmd == '/spslow' else "normal"
            for bot in VALID_BOTS:
                threading.Thread(target=attack_logic, args=(bot, m.chat.id, dan, mode)).start()

        elif cmd == '/spnd':
            if len(args) < 2: return
            stop_event.clear()
            nd = [" ".join(args[1:])]
            for bot in VALID_BOTS:
                threading.Thread(target=attack_logic, args=(bot, m.chat.id, nd)).start()

        # QUẢN TRỊ (ẨN)
        elif cmd == '/ad' and is_admin(uid):
            master.reply_to(m, "👑 Quản trị: /addadm, /xoaadm, /getkey, /xoakey")

        elif cmd == '/setdelay' and is_admin(uid):
            try: DELAY_TIME = float(args[1]); master.reply_to(m, f"⏳ Tốc độ: {DELAY_TIME}s")
            except: pass

        elif cmd == '/cam' and is_admin(uid):
            try:
                target = m.reply_to_message.from_user.id if m.reply_to_message else int(args[1])
                if m.chat.id not in BLACKLIST: BLACKLIST[m.chat.id] = []
                BLACKLIST[m.chat.id].append(target)
                master.reply_to(m, f"🔇 khóa mõm `{target}`")
            except: pass

    master.infinity_polling()

def filter_system():
    global VALID_BOTS
    for t in RAW_TOKENS:
        try:
            bot = telebot.TeleBot(t, threaded=False); bot.get_me()
            VALID_BOTS.append(bot)
        except: pass

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()
    filter_system(); start_master()
