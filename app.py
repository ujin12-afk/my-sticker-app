import streamlit as st
from PIL import Image
import os
import base64

# 로고 이미지를 HTML에 넣기 위해 base64로 변환하는 함수
def get_image_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 1. 페이지 설정
st.set_page_config(page_title="Jazz UP Your Soul", layout="centered")

# 2. 배경색 및 디자인 설정
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f96c88;
    }
    .title-wrapper {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px; /* 로고와 글자 사이 간격 */
        margin-bottom: 25px;
        width: 100%;
    }
    .main-title {
        font-size: clamp(20px, 6vw, 26px); /* 모바일 대응 크기 */
        font-weight: bold;
        color: white;
        margin: 0;
        padding: 0;
        white-space: nowrap;
        line-height: 1.2;
    }
    .logo-img {
        height: clamp(20px, 6vw, 26px); /* 제목 글자 크기와 동일하게 맞춤 */
        width: auto;
    }
    .sub-title {
        font-size: 15px;
        color: #ffe0e6;
        text-align: center;
        margin-top: -15px;
        margin-bottom: 30px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# 3. 로고와 제목을 한 줄로 표시
logo_path = "melonticketlogo.png"

if os.path.exists(logo_path):
    logo_base64 = get_image_base64(logo_path)
    st.markdown(
        f"""
        <div class='title-wrapper'>
            <img src='data:image/png;base64,{logo_base64}' class='logo-img'>
            <h1 class='main-title'>Jazz UP Your Soul</h1>
        </div>
        <p class='sub-title'>프사에 서재페 스티커 붙이기</p>
        """, 
        unsafe_allow_html=True
    )
else:
    # 로고 파일이 없을 경우 제목만 표시
    st.markdown(
        """
        <div class='title-wrapper'>
            <h1 class='main-title'>Jazz UP Your Soul</h1>
        </div>
        <p class='sub-title'>프꾸 w.서울재즈페스티벌</p>
        """, 
        unsafe_allow_html=True
    )

# 4. 사진 업로드
uploaded_file = st.file_uploader("꾸밀 프로필을 선택해주세요!", type=['png', 'jpg', 'jpeg'])

# 5. 업로드 항목 하단 포스터 삽입
if not uploaded_file:
    st.write("---")
    if os.path.exists("SJFposter.png"):
        poster = Image.open("SJFposter.png")
        st.image(poster, caption="Seoul Jazz Festival 2026", use_container_width=True)

# 6. 이미지 합성 로직
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

            st.image(result_img, caption="완성된 프사입니다!", use_container_width=True)

            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            st.download_button(
                label="📥 원형 프사 다운로드 (PNG)",
                data=buf.getvalue(),
                file_name="sjf_profile.png",
                mime="image/png"
            )
