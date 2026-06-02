import streamlit as st
import google.generativeai as genai

# --- ЖИ КІЛТІН БАПТАУ ---
# НАЗАР АУДАРЫҢЫЗ: ОСЫ_ЖЕРГЕ ai.google.dev сайтынан алған өз кілтіңізді қойыңыз
GEMINI_API_KEY = "Google Gemini API" 
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="ЖИ Мамандық", page_icon="🎯", layout="centered")

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# --- 1-ЭКРАН: СӘЛЕМДЕСУ ---
if st.session_state.step == 1:
    st.markdown("<h2 style='text-align: center;'>🎯 ЖИ Негізінде Мамандық Тандау ЖҮЙЕСІ</h2>", unsafe_allow_html=True)
    st.write("Болашақ мамандығыңызды жасанды интеллект көмегімен анықтаңыз. Сұрақтарға жауап беріңіз.")
    st.markdown("---")
    if st.button("Бастау 🚀", use_container_width=True, type="primary"):
        st.session_state.step = 2
        st.rerun()

# --- 2-ЭКРАН: ПӘНДЕРДІ ТАҢДАУ ---
elif st.session_state.step == 2:
    st.subheader("1-Қадам: Өзіңізге ұнайтын пәндерді таңдаңыз")
    subjects = st.multiselect(
        "Қай пәндерді оқыған ұнайды?:",
        ["Математика", "Физика", "Информатика", "Химия", "Биология", "География", "Тарих", "Әдебиет", "Шет тілі"]
    )
    st.markdown("---")
    if st.button("Келесі қадам ➡️", use_container_width=True, type="primary"):
        if subjects:
            st.session_state.answers['subjects'] = ", ".join(subjects)
            st.session_state.step = 3
            st.rerun()
        else:
            st.warning("Жалғастыру үшін кем дегенде бір пән таңдаңыз!")

# --- 3-ЭКРАН: ХОББИ ---
elif st.session_state.step == 3:
    st.subheader("2-Қадам: Өзіңіз туралы ақпарат")
    hobby = st.text_input("Бос уақытыңызда немен айналысқанды ұнатасыз?:", placeholder="Мысалы: сурет салу, код жазу, кітап оқу...")
    st.markdown("---")
    if st.button("Нәтижені алу 🤖✨", use_container_width=True, type="primary"):
        if hobby:
            st.session_state.answers['hobby'] = hobby
            st.session_state.step = 4
            st.rerun()
        else:
            st.warning("Хоббиіңізді жазыңыз!")

# --- 4-ЭКРАН: ЖИ ҚОРЫТЫНДЫСЫ ---
elif st.session_state.step == 4:
    st.subheader("🎯 ЖИ Сараптамасының Қорытындысы")
    
    user_profile = f"Пәндері: {st.session_state.answers['subjects']}. Хоббиі: {st.session_state.answers['hobby']}."
    prompt = f"Сен кәсіптік бағдар бекерші ЖИ-сің. Мына оқушыға Қазақстан нарығына сай ТОП-3 мамандық ұсынып, себебін қысқаша ғылыми негездеп жаз: {user_profile}. Тек қазақ тілінде жауап бер."
    
    with st.spinner("ЖИ мәліметтерді талдауда..."):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error("ЖИ-ге қосылу мүмкін болмады. API кілтін тексеріңіз.")
            
    st.markdown("---")
    if st.button("Қайтадан бастау 🔄", use_container_width=True):
        st.session_state.step = 1
        st.session_state.answers = {}
        st.rerun()

