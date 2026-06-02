import streamlit as st
import google.generativeai as genai
import streamlit as st
import google.generativeai as genai

# Кілтті Streamlit Secrets-тен автоматты түрде алу
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Кілтті Streamlit Secrets-тен автоматты түрде алу
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
st.set_page_config(page_title="ЖИ Мамандық", page_icon="🎯", layout="centered")
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if st.session_state.step == 1:
    st.markdown("<h2 style='text-align: center;'>🎯 ЖИ Негізінде Maмандық Таңдау ЖҮЙЕСІ</h2>", unsafe_allow_html=True)
    st.write("Болашақ мамандығыңызды жасанды интеллект көмегімен анықтаңыз. Сұрақтарға жауап беріңіз.")
    st.markdown("---")
    if st.button("Бастау 🚀", use_container_width=True, type="primary"):
        st.session_state.step = 2
        st.rerun()
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
elif st.session_state.step == 4:
    st.subheader("🎯 ЖИ Сараптамасының Қорытындысы")
    user_profile = f"Пәндері: {st.session_state.answers['subjects']}. Хоббиі: {st.session_state.answers['hobby']}."
    prompt = f"Сен кәсіптік бағдар беруші ЖИ-сің. Мына оқушыға Қазақстан нарығына сай ТОП-3 maмандық ұсынып, себебін қысқаша ғылыми негіздеп жаз: {user_profile}. Тек қазақ тілінде жауап бер."
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
