import streamlit as st
from PIL import Image, ImageOps, ImageDraw
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

# 3. 디자인 및 레이아웃 설정 (CSS)
st.markdown(
    """
    <style>
    /* 전체 배경색 분홍색 */
    .stApp {
        background-color: #f96c88;
    }
    
    /* 오른쪽 상단 로고 (아주 작게 35px) */
    .top-right-logo {
        position: absolute;
        top: 5px;
        right: 10px;
        z-index: 100;
    }
    .top-right-logo img {
        width: 35px; 
        height: auto;
        opacity: 0.8;
    }

    /* 제목 영역 */
    .header-container {
        width: 100%;
        text-align: center;
        margin-top: 30px;
        margin-bottom: 25px;
        padding: 0 10px;
    }
    
    .main-title {
        /* 화면 너비에 따라 글자 크기 자동 조절 (한 줄 유지) */
        font-size: clamp(18px, 7vw, 22px); 
        font-weight: bold;
        color: white !important;
        margin: 0;
        padding: 0;
        line-height: 1.2;
        white-space: nowrap; 
    }
    
    .sub-title {
        font-size: 14px;
        color: #ffe0e6;
        text-align: center;
        margin-top: 8px;
    }
    
    /* 업로드 안내 문구 흰색 */
    .stFileUploader label {
        color: white !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 4. 우측 상단 로고 실제 배치
logo_path = "melonticketlogo.png"
if os.path.exists(logo_path):
    logo_base64 = get_image_base64(logo_path)
    st.markdown(f"<div class='top-right-logo'><img src='data:image/png;base64,{logo_base64}'></div>", unsafe_allow_html=True)

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

# 6. 사진 업로드 창
uploaded_file = st.file_uploader("프로필 사진을 넣어주세요!", type=['png', 'jpg', 'jpeg'])

# 7. 하단 포스터 (사진 올리기 전 상태)
poster_path = "SJFposter.png"
target_url = "https://tktapi.melon.com/gate/landing.json?type=perf&contId=212811"

if not uploaded_file:
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists(poster_path):
        # 이미지를 base64로 변환해서 HTML로 뿌려줍니다 (클릭 가능하게)
        poster_base64 = get_image_base64(poster_path)
        st.markdown(
            f"""
            <a href="{target_url}" target="_blank">
                <img src="data:image/png;base64,{poster_base64}" style="width:100%; border-radius:10px;">
            </a>
            <p style='text-align:center; color:#ffe0e6; font-size:12px; margin-top:5px;'>
                👆 포스터를 클릭하면 예매 페이지로 이동합니다!
            </p>
            """, 
            unsafe_allow_html=True
        )

# 8. 이미지 합성 로직 (사진 업로드 시 작동)
if uploaded_file:
    with st.spinner('스티커 입히는 중...🎷'):
        # --- [STEP 1: 원본 이미지 불러오기 & 방향 보정] ---
        temp_img = Image.open(uploaded_file)
        
        # ⭐ 진짜 완벽 해결 포인트: 사진의 EXIF 회전 정보를 확인해서 똑바로 세워줍니다!
        base_img = ImageOps.exif_transpose(temp_img).convert("RGBA")
        
        # --- [STEP 2: 원형 프사 크롭 및 스티커 합성] ---
        # (이후 로직은 기존과 동일하지만 전체 교체를 위해 포함합니다)
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

                # --- [STEP 3: 최종 결과 출력 및 다운로드] ---
                st.image(result_img, caption="짜잔! 완성된 프사입니다! ✨", use_container_width=True)

                buf = io.BytesIO()
                result_img.save(buf, format="PNG")
                st.download_button(
                    label="📥 원형 프사 다운로드 (PNG)",
                    data=buf.getvalue(),
                    file_name="sjf_profile_result.png",
                    mime="image/png"
                )
