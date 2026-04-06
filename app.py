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

# 3. 디자인 및 레이아웃 설정
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f96c88;
    }
    
    /* 오른쪽 상단 로고 */
    .top-right-logo {
        position: absolute;
        top: 10px;
        right: 15px;
        z-index: 100;
    }
    .top-right-logo img {
        width: 35px;
        height: auto;
    }

    /* 제목 컨테이너 */
    .header-container {
        width: 100%;
        text-align: center;
        margin-top: 45px;
        margin-bottom: 25px;
        padding: 0 20px;
    }
    
    /* 메인 제목 (28px로 상향 조정) */
    .fix-main-title {
        font-size: 28px !important; 
        font-weight: 800 !important;
        color: white !important;
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.1 !important;
        white-space: nowrap !important;
        display: block !important;
    } /* 👈 아까 여기서 이 중괄호가 빠져있었어요! */

    /* 부제목 */
    .fix-sub-title {
        font-size: 14px !important;
        color: #ffe0e6 !important;
        text-align: center !important;
        margin-top: 10px !important;
        display: block !important;
        opacity: 1 !important;
    }
    
    /* '프로필 사진을 넣어주세요' 라벨 및 내부 텍스트 강제 흰색 고정 */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] label p {
        color: white !important;
    }

    /* 업로드 박스 안의 작은 안내 문구들까지 흰색 계열로 */
    [data-testid="stFileUploadDropzone"] div {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 4. 제목 및 로고 실제 표시
logo_path = "melonticketlogo.png"
if os.path.exists(logo_path):
    logo_base64 = get_image_base64(logo_path)
    st.markdown(f"<div class='top-right-logo'><img src='data:image/png;base64,{logo_base64}'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class='header-container'>
        <div class='fix-main-title'>Jazz UP Your Soul</div>
        <div class='fix-sub-title'>프꾸 w.서울재즈페스티벌</div>
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
                포스터를 클릭하면 예매 페이지로 이동합니다.
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
                st.image(result_img, caption="완성된 프로필 사진을 적용해보세요 🕺🏻", use_container_width=True)

                buf = io.BytesIO()
                result_img.save(buf, format="PNG")
                st.download_button(
                    label="📥 원형 프사 다운로드",
                    data=buf.getvalue(),
                    file_name="sjf_profile_result.png",
                    mime="image/png"
                )
