import streamlit as st
from PIL import Image
import os
import io

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="Jazz UP Your Soul ♫", layout="centered")
st.markdown(
    """
    <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; margin-bottom: 30px;'>
        <h1 style='text-align: center; font-size: 28px; white-space: nowrap; margin: 0; padding-right: 10px;'>
            Jazz UP Your Soul ♫
        </h1>
        <p style='text-align: center; font-size: 16px; color: #666; margin-top: 5px;'>
            프사에 서재페 스티커 붙이기
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# 2. 사진 업로드 (업로드되는 순간 아래 코드들이 실행됩니다)
uploaded_file = st.file_uploader("꾸밀 프로필을 선택해주세요!", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # 로딩 메시지 (잠시만 기다려주세요)
    with st.spinner('예쁘게 꾸미는 중...🎷'):
        # 원본 이미지 불러오기
        base_img = Image.open(uploaded_file).convert("RGBA")

        sticker_dir = "stickers"
        
        # 스티커 파일 존재 확인
        if not os.path.exists(sticker_dir) or not os.listdir(sticker_dir):
            st.error("'stickers' 폴더에 PNG 파일을 넣어주세요!")
        else:
            # 스티커 가져오기 (첫 번째 파일)
            all_stickers = sorted([f for f in os.listdir(sticker_dir) if f.lower().endswith('.png')])
            chosen_sticker = all_stickers[0]
            
            sticker_path = os.path.join(sticker_dir, chosen_sticker)
            sticker_img = Image.open(sticker_path).convert("RGBA")

            # 3. 1:1 비율로 크기 조절 및 합성
            sticker_img = sticker_img.resize(base_img.size, Image.LANCZOS)

            result_img = Image.new("RGBA", base_img.size)
            result_img.paste(base_img, (0, 0))
            result_img.paste(sticker_img, (0, 0), sticker_img)

            # 4. 결과 즉시 보여주기
            st.image(result_img, caption="짜잔! 서재페 프꾸가 완성되었습니다.", use_container_width=True)

            # 5. 다운로드 버튼
            buf = io.BytesIO()
            result_img.convert("RGB").save(buf, format="JPEG")
            st.download_button(
                label="📥 NEW 프로필 다운로드",
                data=buf.getvalue(),
                file_name="jazz_up_profile.jpg",
                mime="image/jpeg"
            )
