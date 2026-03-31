import streamlit as st
import json
import os
from gtts import gTTS
import base64

# --- HÀM HỖ TRỢ ---
def load_data():
    """Tải dữ liệu từ file JSON"""
    if os.path.exists('vocab.json'):
        with open('vocab.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def speak(text):
    """Phát âm tiếng Trung"""
    try:
        tts = gTTS(text=text, lang='zh-cn')
        tts.save("temp_audio.mp3")
        with open("temp_audio.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
    except:
        st.error("Lỗi kết nối âm thanh.")

# --- GIAO DIỆN ---
st.set_page_config(page_title="HSK4 Master", layout="wide")

# Tự động load dữ liệu
vocab_data = load_data()

if not vocab_data:
    st.error("⚠️ Không tìm thấy file 'vocab.json'! Hãy chạy file converter trước.")
else:
    # Quản lý trạng thái từ vựng
    if 'idx' not in st.session_state:
        st.session_state.idx = 0
    
    curr = vocab_data[st.session_state.idx]

    # --- HIỂN THỊ NỘI DUNG ---
    st.title("🏮 Học HSK 4 Thông Minh")
    st.markdown(f"**Tiến độ:** {st.session_state.idx + 1} / {len(vocab_data)}")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f"<h1 style='font-size: 80px; color: #E63946;'>{curr['word']}</h1>", unsafe_allow_html=True)
        st.subheader(f"Pinyin: {curr['pinyin']}")
        st.info(f"**Nghĩa:** {curr['meaning']}")
        
        if st.button("🔊 Nghe phát âm"):
            speak(curr['word'])
            
        with st.expander("💡 Mẹo nhớ bộ thủ", expanded=True):
            st.write(curr['story'])
            
        with st.expander("📖 Câu ví dụ", expanded=True):
            st.write(curr['example'])
            if st.button("🔊 Nghe ví dụ"):
                speak(curr['example'])

    with col2:
        st.write("### ✍️ Thứ tự nét viết")
        
        # SỬ DỤNG VÒNG LẶP ĐỂ VẼ TẤT CẢ CÁC CHỮ TRONG TỪ
        for char in curr['word']:
            hanzi_writer_html = f"""
            <script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
            <div id="target-{char}" style="display: inline-block; border: 1px solid #ddd; margin: 5px; background: white; border-radius: 10px;"></div>
            <script>
                var writer = HanziWriter.create('target-{char}', '{char}', {{
                    width: 200,
                    height: 200,
                    padding: 5,
                    showOutline: true,
                    strokeAnimationSpeed: 1, 
                    delayBetweenStrokes: 300
                }});
                writer.animateCharacter();
            </script>
            """
            st.components.v1.html(hanzi_writer_html, height=220)

    # --- ĐIỀU HƯỚNG ---
    st.divider()
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("⬅️ Trước"):
            st.session_state.idx = (st.session_state.idx - 1) % len(vocab_data)
            st.rerun()
    with c2:
        # Thanh trượt nhảy nhanh đến từ bất kỳ
        selected_idx = st.slider("Nhảy nhanh đến từ:", 1, len(vocab_data), st.session_state.idx + 1)
        if selected_idx != st.session_state.idx + 1:
            st.session_state.idx = selected_idx - 1
            st.rerun()
    with c3:
        if st.button("Sau ➡️"):
            st.session_state.idx = (st.session_state.idx + 1) % len(vocab_data)
            st.rerun()