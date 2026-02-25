import streamlit as st
from datetime import datetime
import random
import io
from gtts import gTTS # Đảm bảo đã chạy: pip install gTTS
from modules.lexi_ai import get_word_info

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Lexi AI", layout="wide")

st.markdown("""
<style>
.main { background-color:#0e1117; }
.card { background:#1e2130; padding:20px; border-radius:15px; margin-bottom:15px; border: 1px solid #383c4a; }
.streak-box {
    background:linear-gradient(90deg,#ff512f,#dd2476);
    padding:15px; border-radius:15px; text-align:center;
    color:white; font-size:20px; font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "word_bank" not in st.session_state: st.session_state.word_bank = []
if "streak" not in st.session_state: st.session_state.streak = 0
if "last_date" not in st.session_state: st.session_state.last_date = None

def update_streak():
    today = datetime.now().date()
    if st.session_state.last_date is None:
        st.session_state.streak = 1
    else:
        delta = (today - st.session_state.last_date).days
        if delta == 1:
            st.session_state.streak += 1
        elif delta > 1:
            st.session_state.streak = 1
    st.session_state.last_date = today

def speak(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format='audio/mp3', autoplay=True)

# ================= SIDEBAR =================
with st.sidebar:
    st.title("🏆 Progress")
    word_count = len(st.session_state.word_bank)
    st.progress(min(word_count/50, 1.0))
    st.write(f"📚 Từ đã lưu: {word_count}")
    st.divider()
    st.subheader("🔓 Kỹ năng")
    if word_count >= 10: st.success("📖 Reading OPEN")
    else: st.info(f"🔒 Reading (Cần {10-word_count})")
    if word_count >= 30: st.success("✍ Writing OPEN")
    else: st.info(f"🔒 Writing (Cần {30-word_count})")

# ================= HEADER =================
st.markdown(f'<div class="streak-box">🔥 Chuỗi học tập: {st.session_state.streak} ngày</div>', unsafe_allow_html=True)
st.title("🤖 Lexi AI Smart Dictionary")

# ================= SEARCH =================
word = st.text_input("Tra từ:")

if word:
    with st.spinner("AI đang phân tích..."):
        data = get_word_info(word)

    if "error" in data:
        st.error(f"Lỗi: {data['error']}")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Tiêu đề & Nút phát âm
        col_header, col_audio = st.columns([4, 1])
        with col_header:
            st.header(f"{word.upper()} /{data.get('phonetic','')}/")
        with col_audio:
            if st.button("🔊 Nghe"):
                speak(word)

        st.write(f"**Từ loại:** {data.get('word_class','')} | **Band:** {data.get('band_level','')}")

        col_en, col_vi = st.columns(2)
        with col_en:
            st.markdown("### 🇬🇧 Definition")
            st.write(data.get("definition_en",""))
        with col_vi:
            st.markdown("### 🇻🇳 Nghĩa tiếng Việt")
            st.write(data.get("definition_vi",""))

        st.markdown("### 🎯 Nuance")
        st.write(data.get("nuance",""))
        

        st.markdown("### 🔗 Collocations")
        st.write(", ".join(data.get("collocations", [])))
        
        st.markdown("### 🌿 Idioms")
        st.write(", ".join(data.get("idioms", [])))
       
        st.markdown("### 🔄 Synonyms")
        st.write(", ".join(data.get("synonyms", [])))
       
        st.markdown("### ❌ Antonyms")
        st.write(", ".join(data.get("antonyms", [])))
       
        st.markdown("### 🌱 Word Family")
        st.write(", ".join(data.get("word_family", [])))

        st.markdown("### 💡 Examples")
        for ex in data.get("examples", []):
            st.info(ex)

        if st.button("💾 Lưu vào Word Bank"):
            if not any(w['word'] == word for w in st.session_state.word_bank):
                st.session_state.word_bank.append({
                    "word": word,
                    "meaning": data.get("definition_vi", "")
                })
                update_streak()
                st.success("Đã lưu!")

        st.markdown('</div>', unsafe_allow_html=True)

# ================= QUIZ =================
st.divider()
st.header("🎮 Practice")

if len(st.session_state.word_bank) >= 4:
    correct = random.choice(st.session_state.word_bank)
    wrong = random.sample([w for w in st.session_state.word_bank if w['word'] != correct['word']], 3)
    options = [correct['meaning']] + [w['meaning'] for w in wrong]
    random.shuffle(options)

    choice = st.radio(f"Nghĩa của {correct['word'].upper()}?", options, index=None)

    if st.button("Kiểm tra"):
        if choice == correct['meaning']:
            st.success("Đúng rồi! Chúc mừng em.")
            update_streak()
        else:
            st.error(f"Sai rồi! Đáp án đúng là: {correct['meaning']}")
else:
    st.info("Cần ít nhất 4 từ để mở quiz luyện tập.")