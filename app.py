import streamlit as st
import json
import os
from gtts import gTTS
import base64
import random

# --- HÀM HỖ TRỢ ---
def load_data():
    if os.path.exists('vocab.json'):
        with open('vocab.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def speak(text):
    try:
        tts = gTTS(text=text, lang='zh-cn')
        tts.save("temp_audio.mp3")
        with open("temp_audio.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
    except:
        st.error("Lỗi phát âm.")

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="HSK4 Master & Quiz", layout="wide")
vocab_data = load_data()

if not vocab_data:
    st.warning("⚠️ Hãy chạy 'converter.py' trước!")
else:
    # Khởi tạo session state
    if 'idx' not in st.session_state: st.session_state.idx = 0
    if 'score' not in st.session_state: st.session_state.score = 0

    # Tạo menu điều hướng: Học tập hoặc Kiểm tra
    menu = st.sidebar.radio("Chế độ:", ["📖 Học từ mới", "📝 Bài tập ôn tập (Quiz)"])

    # --- CHẾ ĐỘ HỌC TẬP ---
    if menu == "📖 Học từ mới":
        curr = vocab_data[st.session_state.idx]
        st.title(f"Từ vựng số {st.session_state.idx + 1}")
        
        col1, col2 = st.columns([1, 1.2])
        with col1:
            st.markdown(f"<h1 style='font-size: 100px; color: #E63946;'>{curr['word']}</h1>", unsafe_allow_html=True)
            st.subheader(f"Pinyin: {curr['pinyin']}")
            if st.button("🔊 Phát âm"): speak(curr['word'])
            st.success(f"**Nghĩa:** {curr['meaning']}")
            with st.expander("💡 Mẹo nhớ & Ví dụ", expanded=True):
                st.write(f"**Bộ thủ:** {curr['story']}")
                st.write(f"**Ví dụ:** {curr['example']}")

        with col2:
            st.write("### ✍️ Thứ tự nét viết")
            stroke_url = f"https://dictionary.writtenchinese.com/chart_render.php?c={curr['word']}"
            st.components.v1.iframe(stroke_url, height=450)

        # Điều hướng
        st.divider()
        b1, b2, b3 = st.columns([1, 2, 1])
        with b1:
            if st.button("⬅️ Trước"):
                st.session_state.idx = (st.session_state.idx - 1) % len(vocab_data)
                st.rerun()
        with b3:
            if st.button("Sau ➡️"):
                st.session_state.idx = (st.session_state.idx + 1) % len(vocab_data)
                if (st.session_state.idx) % 10 == 0 and st.session_state.idx != 0:
                    st.toast("🌟 Bạn đã học được 10 từ! Hãy qua tab Bài tập để ôn nhé!", icon="🔥")
                st.rerun()

    # --- CHẾ ĐỘ BÀI TẬP (QUIZ) ---
    else:
        st.title("📝 Bài tập nối từ (Nghĩa - Hán tự)")
        # Lấy 10 từ gần nhất để làm bài tập
        start_idx = (st.session_state.idx // 10) * 10
        end_idx = min(start_idx + 10, len(vocab_data))
        quiz_words = vocab_data[start_idx:end_idx]
        
        if not quiz_words:
            st.write("Chưa có từ nào để làm bài tập.")
        else:
            st.write(f"Đang ôn tập từ số {start_idx + 1} đến {end_idx}")
            
            # Tạo câu hỏi trắc nghiệm
            for item in quiz_words:
                options = [w['meaning'] for w in quiz_words]
                correct_ans = item['meaning']
                
                user_choice = st.radio(f"Từ **{item['word']}** ({item['pinyin']}) có nghĩa là gì?", 
                                       options=random.sample(options, len(options)), 
                                       key=item['word'])
                
                if st.button(f"Kiểm tra từ {item['word']}"):
                    if user_choice == correct_ans:
                        st.balloons()
                        st.success("Chính xác! 🎉")
                    else:
                        st.error(f"Sai rồi! Đáp án đúng là: {correct_ans}")
            
            st.sidebar.metric("Điểm của bạn", st.session_state.score)

    st.sidebar.markdown(f"**Tiến độ: {st.session_state.idx + 1}/{len(vocab_data)}**")