import streamlit as st
from PIL import Image
import os
import io

st.set_page_config(page_title="1:1 스티커 합성", layout="centered")
st.title("🖼️ 사진 전체 스티커 입히기")

uploaded_file = st.file_uploader("사진을 업로드하세요", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # 1. 원본 이미지 불러오기
    base_img = Image.open(uploaded_file).convert("RGBA")
    st.image(base_img, caption="원본 사진", width=300)

    sticker_dir = "stickers"
    
    if not os.path.exists(sticker_dir) or not os.listdir(sticker_dir):
        st.error("'stickers' 폴더에 PNG 파일을 넣어주세요!")
    else:
        if st.button("스티커 입히기 (1:1 고정) ✨"):
            # 2. 스티커 파일 가져오기 (랜덤 제거, 첫 번째 파일 선택)
            all_stickers = sorted([f for f in os.listdir(sticker_dir) if f.lower().endswith('.png')])
            chosen_sticker = all_stickers[0] # 가장 첫 번째 스티커 사용
            
            sticker_path = os.path.join(sticker_dir, chosen_sticker)
            sticker_img = Image.open(sticker_path).convert("RGBA")

            # 3. 중요!! 스티커를 원본 사진의 [가로, 세로] 크기와 똑같이 강제 조절
            # 이렇게 하면 1:1 비율로 사진 전체를 덮게 됩니다.
            sticker_img = sticker_img.resize(base_img.size, Image.LANCZOS)

            # 4. 합성하기 (좌표를 0, 0으로 고정)
            result_img = Image.new("RGBA", base_img.size)
            result_img.paste(base_img, (0, 0))
            result_img.paste(sticker_img, (0, 0), sticker_img)

            # 5. 결과 출력
            st.image(result_img, caption="합성 완료!", use_container_width=True)

            # 6. 다운로드 버튼
            buf = io.BytesIO()
            result_img.convert("RGB").save(buf, format="JPEG")
            st.download_button("📥 이미지 다운로드", buf.getvalue(), "result.jpg", "image/jpeg")
