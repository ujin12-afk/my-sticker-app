import streamlit as st
from PIL import Image, ImageDraw
import os
import io
import random
import base64

# 1. 로고 처리를 위한 함수 (Base64 인코딩)
def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. 페이지 설정 (탭 제목 및 레이아웃)
st.set_page_config(page_title="Jazz UP Your Soul", layout="centered")

# 3. 디자인 및 레이아웃 설정 (모바일 최적화)
st.markdown(
    """
    <style>
    /* 전체 배경색 변경 (#f96c88) */
    .stApp {
        background-color: #f96c88;
    }
    
    /* 제목 & 로고 영역 (Flexbox) */
    .title-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px; /* 로고와 글자 사이 간격 살짝 줄임 */
        margin-bottom: 20px;
        width: 100%;
        /* ⭐ 핵심: 양옆 여백을 줘서 로고가 화면 끝에 붙어 잘리는 것 방지 */
        padding: 0 20px; 
    }
    
    /* 메인 제목 스타일 (대폭 축소) */
    .main-title {
        /* ⭐ 제목 크기를 이전보다 더 줄였습니다. (기존 22px~28px -> 현재 18px~22px) */
        font-size: clamp(18px, 5vw, 22px); 
        font-weight: bold;
        color: white; /* 분홍 배경에 맞춰 흰색 글씨 */
        margin: 0;
        padding: 0;
        line-height: 1.2;
        /* 긴 제목 대응: 한 줄 유지 */
        white-space: nowrap; 
    }
    
    /* 멜론티켓 로고 스타일 */
    .logo-img {
        /* ⭐ 로고 높이도 줄어든 제목 크기에 맞춰 자동으로 조절됩니다. */
        height: clamp(18px, 5vw, 22px); 
        width: auto; /* 비율 유지 */
    }
    
    /* 부제목 스타일 (프꾸 w.서울재즈페스티벌) */
    .sub-title {
        font-size: 14px; /* 조금 더 작게 */
        color: #ffe0e6;
        text-align: center;
        margin-top: -10px;
        margin-bottom: 30px;
        width: 100%;
    }
    
    /* 업로드 영역 안내 문구 흰색으로 */
    .stFileUploader label {
        color: white !important;
        text-align: left !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 4. 제목 및 로고 표시 (Base64 방식 사용)
logo_path = "melonticketlogo.png"

# '프꾸 w.서울재즈페스티벌' 문구로 부제목 업데이트
sub_title_text = "프꾸 w.서울재즈페스티벌"

if os.path.exists(logo_path):
    # 파일이 있을 경우 로고+제목 HTML 삽입
    logo_base64 = get_image_base64(logo_path)
    st.markdown(
        f"""
        <div class='title-wrapper'>
            <img src='data:image/png;base64,{logo_base64}' class='logo-img'>
            <h1 class='main-title'>Jazz UP Your Soul</h1>
        </div>
        <p class='sub-title'>{sub_title_text}</p>
        """, 
        unsafe_allow_html=True
    )
else:
    # 로고 파일이 없을 경우 제목만 표시 (예비용)
    st.markdown(
        f"""
        <div class='title-wrapper'>
            <h1 class='main-title'>Jazz UP Your Soul</h1>
        </div>
        <p class='sub-title'>{sub_title_text}</p>
        """, 
        unsafe_allow_html=True
    )

# 5. 사진 업로드
uploaded_file = st.file_uploader("꾸밀 프로필을 선택해주세요!", type=['png', 'jpg', 'jpeg'])

# --- 중요: 하단 포스터 로직 (업로드 전 칸 아래 위치) ---
poster_path = "SJFposter.png"

# 사진을 고르기 전 상태에서만 포스터 노출
if not uploaded_file:
    st.markdown("<br>", unsafe_allow_html=True) # 간격 추가
    if os.path.exists(poster_path):
        poster = Image.open(poster_path)
        st.image(poster, use_container_width=True)
    else:
        # 파일이 없을 경우에만 안내 메시지 표시 (에러 대신)
        st.write(f"⚠️ {poster_path} 파일을 찾을 수 없습니다. GitHub 메인(최상위 폴더)에 있는지 확인해주세요!")

# 6. 사진 업로드 시 실행되는 원형 합성 로직 (기존 유지)
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
            chosen_sticker = random.choice(all_stickers)
            sticker_path = os.path.join(sticker_dir, chosen_sticker)
            sticker_img = Image.open(sticker_path).convert("RGBA")
            sticker_img = sticker_img.resize(result_img.size, Image.LANCZOS)
            result_img.paste(sticker_img, (0, 0), sticker_img)

            st.image(result_img, caption="짜잔! 완성된 프사입니다!", use_container_width=True)

            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            st.download_button(
                label="📥 원형 프사 다운로드 (PNG)",
                data=buf.getvalue(),
                file_name="sjf_profile.png",
                mime="image/png"
            )
