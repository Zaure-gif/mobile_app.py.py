import google.generativeai as genai


TELEGRAM_TOKEN = "ОСЫ_ЖЕРГЕ_BOTFATHER-ДАН_АЛҒАН_ТОКЕНДІ_ҚОЙЫҢЫЗ"
GEMINI_API_KEY = "ОСЫ_ЖЕРГЕ_GEMINI_API_КІЛТІН_ҚОЙЫҢЫЗ" # ai.google.dev сайтынан тегін алынады

genai.configure(api_key=GEMINI_API_KEY)

AI_INSTRUCTION = """
Сен - мектеп оқушыларына мамандық таңдауға көмектесетін тәжірибелі ЖИ-психолог және кәсіптік бағдар берушісің.
Сенің міндетің - пайдаланушымен WhatsApp форматындағыдай жылы, сыпайы чат жүргізу.
Сұрақтарды бірден үйіп-төкпей, әр хабарламада 1 ғана сұрақ қой.
Мына кезеңдермен сұра:
1. Оқушының қандай пәндерді жақсы көретінін сұра.
2. Оның хоббиі мен бос уақытында немен айналысатынын сұра.
3. Адамдармен жұмыс істегенді ұната ма, әлде компьютер/техникамен бе?
Осы ақпаратты жинаған соң, Қазақстан нарығына сай келетін ең үздік 3 мамандықты атап, ғылыми негіздеме бер.
Тек қазақ тілінде жауап бер.
"""

# Пайдаланушылардың чат тарихын сақтауға арналған база
chat_sessions = {}

# --- 2. БОТТЫҢ ЖҰМЫСЫ ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    # Жаңа ЖИ чатын бастау
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=AI_INSTRUCTION
    )
    chat_sessions[user_id] = model.start_chat(history=[])
    
    welcome_text = "Сәлем! 🙋‍♂️ Мен мамандық таңдауға көмектесетін ЖИ-консультантпын. Саған ең ыңғайлы мамандықты табу үшін бірнеше сұрақ қоямын. Бастау үшін өзің жақсы көретін мектеп пәндеріңді жазшы?"
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_chat(message):
    user_id = message.chat.id
    
   
    if user_id not in chat_sessions:
        send_welcome(message)
        return

    try:
      
        chat = chat_sessions[user_id]
        response = chat.send_message(message.text)
        
      
        bot.send_message(user_id, response.text)
    except Exception as e:
        bot.send_message(user_id, "Кешіріңіз, байланыс үзілді. Қайтадан байқап көріңіз.")


print("Бот жұмыс істеп тұр...")
bot.polling()