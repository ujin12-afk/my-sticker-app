import streamlit as st
from PIL import Image, ImageDraw
import os
import io
import random
import base64

# 1. 로고 처리를 위한 함수
def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. 페이지 설정
st.set_page_config(page_title="Jazz UP Your Soul", layout="centered")

# 3. 디자인 및 레이아웃 설정
# 배경색 #f96c88, 제목/자막 색상 #ffe0e6 통일
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f96c88;
    }
    
    /* 오른쪽 상단 로고 고정 스타일 */
    .top-right-logo {
        position: absolute;
        top: 10px;
        right: 15px;
        z-index: 100;
    }
    .top-right-logo img {
        width: 80px; /* 로고 크기 조절 */
        height: auto;
    }

    /* 제목 영역 */
    .header-container {
        width: 100%;
        text-align: center;
        margin-top: 40px; /* 로고와 겹치지 않게 상단 여백 추가 */
        margin-bottom: 25px;
    }
    
    .main-title {
        font-size: clamp(24px, 7vw, 32px);
        font-weight: bold;
        color: white
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }
    
    .sub-title {
        font-size: 16px;
        color: #ffe0e6;
        text-align: center;
        margin-top: 10px;
    }
    
    .stFileUploader label {
        color: white !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 4. 우측 상단 로고 배치
logo_path = "melonticketlogo.png"
if os.path.exists(logo_path):
    logo_base64 = get_image_base64(logo_path)
    st.markdown(
        f"""
        <div class="top-right-logo">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
        """, 
        unsafe_allow_html=True
    )

# 5. 중앙 제목 및 자막 표시
st.markdown(
    """
    <div class='header-container'>
        <h1 class='main-title'>Jazz UP Your Soul</h1>
        <p class='sub-title'>프꾸 w.서울재즈페스티벌</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# 6. 사진 업로드
uploaded_file = st.file_uploader("꾸밀 프로필을 선택해주세요!", type=['png', 'jpg', 'jpeg'])

# 7. 하단 포스터 (업로드 전 노출)
poster_path = "SJFposter.png"
if not uploaded_file:
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists(poster_path):
        poster = Image.open(poster_path)
        st.image(poster, use_container_width=True)

# 8. 이미지 합성 로직
if uploaded_file:
    with st.spinner('랜덤 스티커 입히는 중...🎷'):
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

        sticker_dir = "stickers"
        if os.path.exists(sticker_dir) and os.listdir(sticker_dir):
            all_stickers = [f for f in os.listdir(sticker_dir) if f.lower().endswith('.png')]
            if all_stickers:
                chosen_sticker = random.choice(all_stickers)
                sticker_path = os.path.join(sticker_dir, chosen_sticker)
                sticker_img = Image.open(sticker_path).convert("RGBA")
                sticker_img = sticker_img.resize(result_img.size, Image.LANCZOS)
                result_img.paste(sticker_img, (0, 0), sticker_img)

                st.image(result_img, caption="완성된 프사입니다! ✨", use_container_width=True)

                buf = io.BytesIO()
                result_img.save(buf, format="PNG")
                st.download_button(
                    label="📥 원형 프사 다운로드 (PNG)",
                    data=buf.getvalue(),
                    file_name="sjf_profile.png",
                    mime="image/png"
                )
