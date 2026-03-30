import pandas as pd
from pypinyin import pinyin, Style
import json
import os

def get_rich_data(word):
    # Thư viện dữ liệu mẫu để bổ sung phần "câu chuyện" và "ví dụ"
    # Bạn có thể mở rộng danh sách này trong code
    database = {
        "压力": {
            "story": "Bộ Hán (厂) là vách đá, bên dưới là chữ (压) - vách đá đè nặng lên người.",
            "example": "工作压力很大 (Gōngzuò yālì hěn dà): Áp lực công việc rất lớn."
        },
        "耐心": {
            "story": "Bộ Đao (刀) nằm trên bộ Tâm (心): Nhẫn nại là khi dao đâm vào tim vẫn chịu đựng được.",
            "example": "教育孩子 city xūyào nàixīn (Jiàoyù háizi xūyào nàixīn): Dạy bảo con cái cần sự nhẫn nại."
        }
    }
    return database.get(word, {
        "story": f"Chữ '{word}' được cấu tạo từ các bộ thủ tượng hình. Hãy quan sát hình dáng để nhớ nghĩa.",
        "example": f"我正在学习 '{word}' 这个词 (Wǒ zhèngzài xuéxí zhège cí): Tôi đang học từ này."
    })

def run_conversion():
    file_name = 'TuVungHSK4.xlsx'
    if not os.path.exists(file_name):
        print(f"❌ Không tìm thấy file {file_name} trong thư mục!")
        return

    print("⏳ Đang xử lý dữ liệu từ Excel...")
    df = pd.read_excel(file_name)
    
    # Kiểm tra tên cột trong Excel của bạn (HanTu và Nghia)
    json_data = []
    for _, row in df.iterrows():
        hantu = str(row['HanTu'])
        nghia = str(row['Nghia'])
        
        # Tự động tạo Pinyin có dấu
        py = "".join([item[0] for item in pinyin(hantu, style=Style.TONE)])
        
        # Lấy câu chuyện và ví dụ
        extra = get_rich_data(hantu)
        
        json_data.append({
            "word": hantu,
            "pinyin": py,
            "meaning": nghia,
            "story": extra['story'],
            "example": extra['example']
        })

    with open('vocab.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print("✅ Đã tạo xong file 'vocab.json'. Bây giờ bạn có thể mở App!")

if __name__ == "__main__":
    run_conversion()