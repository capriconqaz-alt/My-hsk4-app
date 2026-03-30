import streamlit as st

# Dữ liệu từ vựng Ngày 1 được bổ sung câu ví dụ
vocab_data = [
    {
        "word": "压力",
        "pinyin": "yālì",
        "meaning": "Áp lực",
        "story": "Bộ Hán (厂) như vách đá đè lên trên đầu.",
        "example": "工作压力很大 (Gōngzuò yālì hěn dà) - Áp lực công việc rất lớn.",
        "stroke_gif": "https://raw.githubusercontent.com/googlei18n/noto-emoji/master/third_party/region-flags/svg/CN.svg" # Demo link
    },
    {
        "word": "耐心",
        "pinyin": "nàixīn",
        "meaning": "Nhẫn nại",
        "story": "Trái tim (心) nằm dưới lưỡi đao (刃).",
        "example": "教育孩子需要耐心 (Jiàoyù háizi xūyào nàixīn) - Dạy bảo con cái cần sự nhẫn nại.",
        "stroke_gif": "https://raw.githubusercontent.com/googlei18n/noto-emoji/master/third_party/region-flags/svg/CN.svg"
    }
]

st.set_page_config(page_title="HSK4 Smart Learner", layout="wide")

# --- Giao diện ---
st.title("🏮 HSK 4: Học Từ Vựng Thông Minh")

if 'word_index' not in st.session_state:
    st.session_state.word_index = 0

current_word = vocab_data[st.session_state.word_index]

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"## {current_word['word']} ({current_word['pinyin']})")
    st.success(f"**Nghĩa:** {current_word['meaning']}")
    
    with st.expander("💡 Câu chuyện bộ thủ", expanded=True):
        st.write(current_word['story'])
        
    with st.expander("📖 Câu ví dụ", expanded=True):
        st.info(current_word['example'])

with col2:
    st.write("### ✍️ Thứ tự nét viết")
    # Giải pháp tạm thời: Hiển thị hình ảnh minh họa thay vì link động bị lỗi
    # Trong thực tế, bạn hãy tải các file GIF về máy và dùng đường dẫn nội bộ
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJndXIzZ3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6Z3R6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxxXvDS5D3y/giphy.gif", width=300, caption="Minh họa nét vẽ")

# --- Điều hướng ---
st.divider()
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.button("⬅️ Trước"):
        st.session_state.word_index = (st.session_state.word_index - 1) % len(vocab_data)
        st.rerun()
with c3:
    if st.button("Sau ➡️"):
        st.session_state.word_index = (st.session_state.word_index + 1) % len(vocab_data)
        st.rerun()