import streamlit as st
from PIL import Image, ImageDraw
import os
import io
import random
import base64

# 1. 로고 처리를 위한 함수 (이미지를 HTML에 직접 삽입하기 위함)
def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. 페이지 설정
st.set_page_config(page_title="Jazz UP Your Soul", layout="centered")

# 3. 전체 디자인 및 레이아웃 설정 (CSS)
st.markdown(
    """
    <style>
    /* 전체 배경색 설정 */
    .stApp {
        background-color: #f96c88;
    }
    
    /* 제목과 로고를 감싸는 컨테이너 (중앙 정렬 핵심) */
    .header-container {
        width: 100%;
        text-align: center;
        padding: 0 10px;
        margin-bottom: 20px;
    }
    
    /* 로고와 제목을 한 몸처럼 묶음 */
    .title-box {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        max-width: 100%;
    }
    
    .logo-img {
        height: 22px; /* 제목 높이에 맞춘 로고 사이즈 */
        width: auto;
        margin-right: 0px; /* 로고와 텍스트 사이 간격 */
        flex-shrink: 0;
    }
    
    .main-title {
        font-size: 22px;
        font-weight: bold;
        color: white;
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
        margin-bottom: 30px;
    }
    
    /* 업로드 섹션 글자색 흰색 고정 */
    .stFileUploader label {
        color: white !important;
        text-align: left !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 4. 상단 제목 및 로고 표시
logo_path = "melonticketlogo.png"
sub_title_text = "프꾸 w.서울재즈페스티벌"

if os.path.exists(logo_path):
    logo_base64 = get_image_base64(logo_path)
    st.markdown(
        f"""
        <div class='header-container'>
            <div class='title-box'>
                <img src='data:image/png;base64,{logo_base64}' class='logo-img'>
                <h1 class='main-title'>Jazz UP Your Soul</h1>
            </div>
            <p class='sub-title'>{sub_title_text}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"<div class='header-container'><h1 class='main-title'>Jazz UP Your Soul</h1><p class='sub-title'>{sub_title_text}</p></div>", 
        unsafe_allow_html=True
    )

# 5. 사진 업로드 창
uploaded_file = st.file_uploader("꾸밀 프로필을 선택해주세요!", type=['png', 'jpg', 'jpeg'])

# 6. 하단 포스터 표시 (업로드 전 상태에서만 노출)
poster_path = "SJFposter.png"
if not uploaded_file:
    st.markdown("<br>", unsafe_allow_html=True)
    if os.path.exists(poster_path):
        poster = Image.open(poster_path)
        st.image(poster, use_container_width=True)
    else:
        # 파일이 없을 경우 관리자 확인용 안내 (사용자에게는 투명하게 처리하고 싶으면 주석 처리 가능)
        st.info(f"'{poster_path}' 파일을 찾고 있습니다. GitHub 최상위 폴더에 업로드 해주세요!")

# 7. 이미지 합성 로직 (사진 업로드 시 작동)
if uploaded_file:
    with st.spinner('랜덤 스티커 입히는 중...🎷'):
        # 원본 이미지 불러오기 및 RGBA 변환
        base_img = Image.open(uploaded_file).convert("RGBA")
        
        # 중앙 기준 정사각형 크롭
        min_dim = min(base_img.size)
        left = (base_img.width - min_dim) // 2
        top = (base_img.height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        cropped_img = base_img.crop((left, top, right, bottom))

        # 원형 마스크 생성 및 자르기
        circle_img = Image.new("RGBA", (min_dim, min_dim), (255, 255, 255, 0))
        mask = Image.new("L", (min_dim, min_dim), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, min_dim, min_dim), fill=255)
        result_img = Image.composite(cropped_img, circle_img, mask)

        # 랜덤 스티커 선택 및 합성
        sticker_dir = "stickers"
        if os.path.exists(sticker_dir) and os.listdir(sticker_dir):
            all_stickers = [f for f in os.listdir(sticker_dir) if f.lower().endswith('.png')]
            if all_stickers:
                chosen_sticker = random.choice(all_stickers)
                sticker_path = os.path.join(sticker_dir, chosen_sticker)
                sticker_img = Image.open(sticker_path).convert("RGBA")
                
                # 스티커를 결과 이미지 크기에 1:1로 맞춤
                sticker_img = sticker_img.resize(result_img.size, Image.LANCZOS)
                result_img.paste(sticker_img, (0, 0), sticker_img)

                # 최종 이미지 출력
                st.image(result_img, caption="짜잔! 완성된 프사입니다! ✨", use_container_width=True)

                # 다운로드 버튼 (PNG 유지)
                buf = io.BytesIO()
                result_img.save(buf, format="PNG")
                st.download_button(
                    label="📥 원형 프사 다운로드 (PNG)",
                    data=buf.getvalue(),
                    file_name="sjf_profile_result.png",
                    mime="image/png"
                )
            else:
                st.warning("stickers 폴더 내에 PNG 파일이 없습니다.")
        else:
            st.warning("stickers 폴더를 찾을 수 없습니다.")
