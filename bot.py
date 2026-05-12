import telebot, threading, time, random, os, json, uuid
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

# --- NẠP NGÔN ---
def get_ngon_tu():
    all_lines = []
    for fname in ["ngontagtele.txt", "chui.txt"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as f:
                for line in f:
                    clean = line.strip()
                    if clean and not clean.startswith("["): all_lines.append(clean)
    if not all_lines: all_lines = ["Hai Quy NO1"]
    chunk = max(1, len(all_lines) // 4)
    return {"sp": all_lines[:chunk], "sp2": all_lines[chunk:chunk*2], "sptag": all_lines[chunk*2:chunk*3], "spslow": all_lines[chunk*3:]}

KHO_DAN = get_ngon_tu()
def is_admin(uid): return uid in db["admins"] or uid == OWNER_ID

# --- LOGIC TẤN CÔNG ---
def attack_logic(bot, chat_id, lines, mode="normal"):
    while not stop_event.is_set():
        try:
            bot.send_message(chat_id, random.choice(lines))
            time.sleep(DELAY_TIME if mode == "normal" else 2.5)
        except: break

def start_master():
    if not VALID_BOTS: return
    master = VALID_BOTS[0]

    @master.message_handler(func=lambda m: True)
    def handle_all(m):
        global DELAY_TIME, stop_event, BLACKLIST, db
        uid, gid = m.from_user.id, m.chat.id
        args = m.text.split()
        if not args: return
        cmd = args[0].lower()

        if gid in BLACKLIST and uid in BLACKLIST[gid]:
            try: master.delete_message(gid, m.message_id)
            except: pass
            return

        # --- MENU CHO NGƯỜI KHÁC THẤY (HÀNG DỌC) ---
        if cmd == '/help':
            master.reply_to(m, (
                "───「 **HAI QUY 2026** 」───\n"
                "🔥 **𝐒𝐏𝐀𝐌 & 𝐓𝐀𝐆**\n"
                "┣ `/sp` - Spam ngôn \n"
                "┣ `/sp2` - Spam ngôn \n"
                "┣ `/sptag` - Tag ẩn đối thủ\n"
                "┣ `/spslow` - Spam chậm\n"
                "┗ `/spnd` - Spam nội dung\n\n"
                "☠️ **𝐐𝐔𝐀̉𝐍 𝐋𝐘́ 𝐂𝐇𝐀𝐓**\n"
                "┣ `/cam` - Khóa mõm\n"
                "┣ `/sua` - Tháo rọ mõm\n"
                "┣ `/clear` -XOA TIN NHAN\n"
                "┗ `/setdelay` - Chỉnh tốc độ\n\n"
                "📦 **𝐓𝐈𝐄̣̂𝐍 𝐈́𝐂𝐇**\n"
                "┣ `/dung` - STOP\n"
                "┣ `/listbot` - Check BOT\n"
                "┣ `/setkey` - NHAP KEY\n"
                "┗ `/info` - Check thông tin\n"
                "──────────────────\n"
                "👤 **OWNER:** Hải Quý"
            ), parse_mode="Markdown")

        # --- MENU CHỈ ADMIN THẤY ---
        elif cmd == '/ad':
            if is_admin(uid):
                master.reply_to(m, (
                    "───「 **ADMIN CONTROL** 」───\n"
                    "👑 **𝐐𝐔𝐘𝐄̂̀𝐍 𝐓𝐎̂́𝐈 𝐂𝐀𝐎**\n"
                    "┣ `/addadm <id>` - Thêm Admin\n"
                    "┣ `/xoaadm <id>` - Xóa Admin\n"
                    "┣ `/newkey <tên> <day/week/month/forever>`\n"
                    "┗ `/xoakey <tên>` - Xóa Key bot\n"
                    "──────────────────"
                ), parse_mode="Markdown")
            else:
                master.reply_to(m, "⚠️ **Cảnh báo:** Bạn không có quyền sử dụng lệnh này!")

        elif cmd == '/info':
            master.reply_to(m, f"👤 **Tên:** {m.from_user.first_name}\n🆔 **ID:** `{uid}`\n🌐 **Chat ID:** `{gid}`", parse_mode="Markdown")
        elif cmd == '/listbot':
            master.reply_to(m, f"🤖 **Bot Online:** {len(VALID_BOTS)}/29")
        elif cmd in ['/sp', '/sp2', '/sptag', '/spslow']:
            stop_event.clear()
            dan = KHO_DAN.get(cmd[1:], KHO_DAN['sp'])
            for b in VALID_BOTS: threading.Thread(target=attack_logic, args=(b, gid, dan, "slow" if cmd == '/spslow' else "normal")).start()
        elif cmd == '/spnd' and len(args) > 1:
            stop_event.clear()
            nd = [" ".join(args[1:])]
            for b in VALID_BOTS: threading.Thread(target=attack_logic, args=(b, gid, nd)).start()
        elif cmd == '/dung':
            stop_event.set(); master.reply_to(m, "🛑 **STOP!**")

        # LOGIC XỬ LÝ LỆNH ẨN
        elif is_admin(uid):
            if cmd == '/addadm' and len(args) > 1:
                new_id = int(args[1])
                if new_id not in db["admins"]: 
                    db["admins"].append(new_id); save_data(db)
                    master.reply_to(m, f"✅ Đã thêm Admin: `{new_id}`")
            elif cmd == '/xoaadm' and len(args) > 1:
                old_id = int(args[1])
                if old_id in db["admins"]: 
                    db["admins"].remove(old_id); save_data(db)
                    master.reply_to(m, f"❌ Đã xóa Admin: `{old_id}`")
            elif cmd == '/newkey' and len(args) > 2:
                key_name, duration = args[1], args[2].lower()
                days = {"day": 1, "week": 7, "month": 30, "forever": 36500}.get(duration, 1)
                expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
                db["keys"][key_name] = expiry; save_data(db)
                master.reply_to(m, f"🔑 **Key:** `{key_name}` | ⏰ **Hết hạn:** {expiry}")
            elif cmd == '/xoakey' and len(args) > 1:
                key_del = args[1]
                if key_del in db["keys"]: 
                    del db["keys"][key_del]; save_data(db)
                    master.reply_to(m, f"🗑️ Đã xóa Key: `{key_del}`")
            elif cmd == '/setdelay' and len(args) > 1:
                try: DELAY_TIME = float(args[1]); master.reply_to(m, f"⏳ Tốc độ: {DELAY_TIME}s")
                except: pass
            elif cmd == '/cam':
                target = m.reply_to_message.from_user.id if m.reply_to_message else (int(args[1]) if len(args)>1 else None)
                if target:
                    if gid not in BLACKLIST: BLACKLIST[gid] = []
                    BLACKLIST[gid].append(target); master.reply_to(m, f"🔇 Khóa mõm `{target}`")
            elif cmd == '/sua':
                target = m.reply_to_message.from_user.id if m.reply_to_message else (int(args[1]) if len(args)>1 else None)
                if target and gid in BLACKLIST and target in BLACKLIST[gid]:
                    BLACKLIST[gid].remove(target); master.reply_to(m, f"🐶 Tháo rọ `{target}`")
            elif cmd == '/clear':
                master.reply_to(m, "🧹 Dọn rác thành công!")

    master.infinity_polling()

def filter_system():
    for t in RAW_TOKENS:
        try:
            bot = telebot.TeleBot(t, threaded=False); bot.get_me(); VALID_BOTS.append(bot)
        except: pass

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()
    filter_system(); start_master()
