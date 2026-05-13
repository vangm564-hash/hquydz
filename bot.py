import telebot, threading, time, random, os, json
from datetime import datetime, timedelta
from flask import Flask

app = Flask(__name__)
@app.route('/')
def home(): return "HAI QUY BOT SYSTEM ONLINE"

DATA_FILE = "bot_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    return {"admins": [7153197678], "keys": {}, "users_with_key": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

db = load_data()
OWNER_ID = 7153197678 
DELAY_TIME = 0.1 # Mặc định 0.1 giây
stop_event = threading.Event()

RAW_TOKENS = ['8675065386:AAHVtY8NYQOykrCCEQ9tQDpe_mZK9XUmVV0', '8750639984:AAGAU7SsEe_V9CpZ9LAfxovI2iFWSCQ9riw', '8423233437:AAFPeFNFctZlgO8VU_KGkp_HT71FCTywUmI', '8705345450:AAHAxsFUHu7ux4USLvItL018KD4hBsTe4_Q', '8144155270:AAH-y47kIAFWgo7sge1VmCMrx2dc9CkYxOs', '8688293059:AAGoga_q3E7VbZQ3sL6xZ3-vzGgtC7RsTmc', '8652311818:AAGmFWSeRYW1-RQ-RH8jNguwkRtzFt0U-oQ', '8731497895:AAHHhCiAp7a62eflQBe0PztWw0jRjDPpyk4', '8684330434:AAEORwA4uvBXIm-orys4txSttOnkH2CRwZ4', '8796842934:AAENmEMod5CHQxfcl6Z5kl3nlwv8slQLJJc', '8668865669:AAGMgG3zBSN69eDYzTHENxl6Y9AAj6Kln4Q', '8429960682:AAHltNvwWjEn1QC_f5R8JPgz7uN1uFhny18', '8481938728:AAGen1t8Tz3jeu02kJ8HoCIZLiPLdd687n8', '8739448460:AAGNLEW-WDvatvatMplzkziG5pd5hTRfqiE', '8689807630:AAEoXvm45QaW1jlT-H_KzNlmCpu50Q3k2S4', '8575475228:AAHRtsOcCEQInRvR3isSBV-Igur-WykB_PE', '8651553692:AAGNQwqUoWgV1QV0ozaZHLRL0RJm9M8q0e0', '8712129360:AAEgW2hBbtsgY8DyMd9mxYw1B6X8_VBpF-g', '8626439785:AAEn2pArlYu0KW9tHLETtrJUXKo2BR0hjx0', '8793582382:AAHfbcee8kt-x6OeLHqwqXP79U4PBaII0MA', '8397463503:AAGajcEI5H_SJ0i6mccvPT7GC-P8U5RTLOQ', '8718672219:AAH37zxnCBuWLMSEW_rCvEwnrf0ym8d7-H0', '8650032681:AAE9TeiIIywG796f6hHLY7JiBWhNgH3gc', '8303481123:AAFN_bijtWzXlR1FlYHEvgN-5uhyqnZsbu0', '8619086108:AAFYqRAdKNvg84eyj1ylXfa-TF8W8o8fxbo', '8661308767:AAFU__yZv8r1HlJ5jaW3URW88bWKWYKDCCY', '8625550674:AAHIHuakDCvvxwCC0mgrDLU5g8vBNFdD7eI', '8724848112:AAHhLYnH1LO4tVUPMTjztbNZZtni7D0uDl4', '8471422557:AAF30BcMF15veQPHCTDqcA1NU0iHb63Zm1o']
VALID_BOTS = []

def is_admin(uid): 
    return uid in db["admins"] or uid == OWNER_ID

def attack_logic(bot, chat_id, lines):
    while not stop_event.is_set():
        try:
            bot.send_message(chat_id, random.choice(lines))
            time.sleep(DELAY_TIME)
        except: break

def start_master():
    if not VALID_BOTS: return
    master = VALID_BOTS[0]

    @master.message_handler(func=lambda m: True)
    def handle_all(m):
        global DELAY_TIME, stop_event, db
        uid, gid = m.from_user.id, m.chat.id
        args = m.text.split()
        if not args: return
        cmd = args[0].lower()

        if cmd == '/help':
            if is_admin(uid):
                msg = (
                    "───「 **HAI QUY 2026** 」───\n"
                    "┣ `/sp` - Spam ngôn chửi\n"
                    "┣ `/spnd` - Spam tự chọn\n"
                    "┣ `/dung` - Dừng spam\n"
                    "┣ `/setdelay` - Chỉnh tốc độ (Admin)\n"
                    "┣ `/ad` - Menu quản trị\n"
                    "┣ `/info` - Lấy ID\n"
                    "┗ `/setkey` - Kích hoạt Key\n"
                    "──────────────────"
                )
            else:
                msg = "───「 **USER** 」───\n┣ `/info` - ID\n┗ Admin: @hquydz"
            master.reply_to(m, msg)

        # --- LỆNH SETDELAY MỚI ---
        elif cmd == '/setdelay' and is_admin(uid):
            try:
                DELAY_TIME = float(args[1])
                master.reply_to(m, f"⚡️ Đã chỉnh Delay về: `{DELAY_TIME}` giây")
            except: master.reply_to(m, "⚠️ Cú pháp: `/setdelay [số giây]` (VD: `/setdelay 0.05`)")

        elif cmd == '/ad' and is_admin(uid):
            master.reply_to(m, "───「 **ADMIN** 」───\n┣ `/addadm`\n┣ `/xoaadm`\n┣ `/newkey`\n┗ `/xoakey`")

        elif cmd == '/addadm' and uid == OWNER_ID:
            try:
                target = m.reply_to_message.from_user.id if m.reply_to_message else int(args[1])
                if target not in db["admins"]:
                    db["admins"].append(target); save_data(db)
                    master.reply_to(m, f"✅ Thêm Admin: `{target}`")
            except: pass

        elif cmd == '/sp' or cmd == '/spnd':
            if is_admin(uid) or str(uid) in db.get("users_with_key", {}):
                stop_event.clear()
                dan = [args[1]] if (cmd == '/spnd' and len(args)>1) else ["Hải Quý NO.1", "Cân cả tgioi"]
                for b in VALID_BOTS: threading.Thread(target=attack_logic, args=(b, gid, dan)).start()

        elif cmd == '/dung' and is_admin(uid):
            stop_event.set(); master.reply_to(m, "🛑 Dừng!")

        elif cmd == '/info':
            target_id = m.reply_to_message.from_user.id if m.reply_to_message else uid
            master.reply_to(m, f"🆔 ID:\n`{target_id}`")

    master.infinity_polling()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port), daemon=True).start()
    for t in RAW_TOKENS:
        try:
            bot = telebot.TeleBot(t, threaded=False); bot.get_me(); VALID_BOTS.append(bot)
        except: pass
    start_master()
