import streamlit as st
from PIL import Image, ImageDraw
import os
import io
import random  # 랜덤 기능을 위해 추가!

# 1. 페이지 설정
st.set_page_config(page_title="Jazz UP Your Soul✨", layout="centered")

# 2. 디자인 및 레이아웃 설정 (모바일 최적화)
st.markdown(
    """
    <style>
    .title-container {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 25px;
        padding: 0 5px;
    }
    .main-title {
        font-size: clamp(18px, 6vw, 24px); 
        font-weight: bold;
        margin: 0;
        padding: 0;
        text-align: center;
        white-space: nowrap;
        line-height: 1.2;
        padding-left: 15px; 
    }
    .sub-title {
        font-size: clamp(13px, 4vw, 15px);
        color: #666;
        margin-top: 5px;
        text-align: center;
    }
    .stFileUploader label {
        text-align: left !important;
        display: block !important;
    }
    </style>
    
    <div class='title-container'>
        <h1 class='main-title'>Jazz UP Your Soul✨</h1>
        <p class='sub-title'>프사에 서재페 스티커 붙이기</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# 3. 사진 업로드
uploaded_file = st.file_uploader("꾸밀 프로필을 선택해주세요!", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    with st.spinner('랜덤 스티커 입히는 중...🎷'):
        # --- [STEP 1: 원본 이미지 원형 크롭] ---
        base_img = Image.open(uploaded_file).convert("RGBA")
        min_dim = min(base_img.size)
        left = (base_img.width - min_dim) // 2
        top = (base_img.height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        cropped_img = base_img.crop((left, top, right, bottom))

        circle_img = Image.new("RGBA", (min_dim, min_dim), (255, 255, 255, 0))
        mask = Image.new("L", (min_dim, min_dim), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, min_dim, min_dim), fill=255)
        result_img = Image.composite(cropped_img, circle_img, mask)

        # --- [STEP 2: 랜덤 스티커 선택] ---
        sticker_dir = "stickers"
        
        if not os.path.exists(sticker_dir) or not os.listdir(sticker_dir):
            st.error("'stickers' 폴더에 PNG 파일을 넣어주세요!")
        else:
            # 폴더 내 모든 PNG 파일 목록 가져오기
            all_stickers = [f for f in os.listdir(sticker_dir) if f.lower().endswith('.png')]
            
            # ⭐ 랜덤으로 하나 선택!
            chosen_sticker = random.choice(all_stickers)
            
            sticker_path = os.path.join(sticker_dir, chosen_sticker)
            sticker_img = Image.open(sticker_path).convert("RGBA")

            # 스티커 크기 조절 및 합성
            sticker_img = sticker_img.resize(result_img.size, Image.LANCZOS)
            result_img.paste(sticker_img, (0, 0), sticker_img)

            # --- [STEP 3: 결과 출력 및 다운로드] ---
            st.image(result_img, caption=f"랜덤 스티커 적용 완료! ({chosen_sticker})", use_container_width=True)

            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            st.download_button(
                label="📥 원형 프사 다운로드 (PNG)",
                data=buf.getvalue(),
                file_name="sjf_profile_random.png",
                mime="image/png"
            )
