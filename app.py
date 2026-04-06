import streamlit as st
from PIL import Image, ImageDraw
import os
import io

# 1. 페이지 설정
st.set_page_config(page_title="Jazz UP Your Soul✨", layout="centered")

# 2. 디자인 및 레이아웃 설정
# 2. 디자인 및 레이아웃 설정
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
        padding: 0 10px; /* 양옆 여백 추가 */
    }
    .main-title {
        font-size: 24px; /* 크기를 살짝 줄여서 모바일에서 안 잘리게 함 */
        font-weight: bold;
        margin: 0;
        padding: 0;
        text-align: center;
        line-height: 1.2;
        /* 이모지 때문에 왼쪽으로 쏠려 보일 때를 대비한 보정값 */
        padding-left: 20px; 
    }
    .sub-title {
        font-size: 15px;
        color: #666;
        margin-top: 5px;
        text-align: center;
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
    # 합성 중 로딩 표시
    with st.spinner('원형 프사로 변신 중...🎷'):
        # --- [STEP 1: 원본 이미지 처리] ---
        # 원본 이미지 불러오기 (RGBA 모드로 변환)
        base_img = Image.open(uploaded_file).convert("RGBA")
        
        # 정사각형 크기 결정 (가로, 세로 중 짧은 쪽 기준)
        min_dim = min(base_img.size)
        
        # 중앙을 기준으로 정사각형으로 자르기 (Crop)
        left = (base_img.width - min_dim) // 2
        top = (base_img.height - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        cropped_img = base_img.crop((left, top, right, bottom))

        # --- [STEP 2: 원형 마스크 생성 및 자르기] ---
        # 같은 크기의 투명 이미지 만들기
        circle_img = Image.new("RGBA", (min_dim, min_dim), (255, 255, 255, 0))
        
        # 하얀색 원형 마스크 그리기
        mask = Image.new("L", (min_dim, min_dim), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, min_dim, min_dim), fill=255)
        
        # 마스크를 이용해 사진을 원형으로 자르기
        result_img = Image.composite(cropped_img, circle_img, mask)

        # --- [STEP 3: 스티커 합성] ---
        sticker_dir = "stickers"
        
        # stickers 폴더 및 파일 존재 확인
        if not os.path.exists(sticker_dir) or not os.listdir(sticker_dir):
            st.error("'stickers' 폴더에 PNG 스티커 파일을 넣어주세요!")
        else:
            # 첫 번째 스티커 파일 가져오기
            all_stickers = sorted([f for f in os.listdir(sticker_dir) if f.lower().endswith('.png')])
            chosen_sticker = all_stickers[0]
            
            sticker_path = os.path.join(sticker_dir, chosen_sticker)
            sticker_img = Image.open(sticker_path).convert("RGBA")

            # 스티커를 원형 사진 크기에 맞춰 1:1로 조절
            sticker_img = sticker_img.resize(result_img.size, Image.LANCZOS)

            # 이미지 합성 (좌표 0, 0 고정, 원형 가장자리에 맞춤)
            # result_img 자체가 이미 원형이므로, 0,0에 붙이면 꽉 찹니다.
            result_img.paste(sticker_img, (0, 0), sticker_img)

            # --- [STEP 4: 최종 결과 출력 및 다운로드] ---
            # 결과물 출력 (use_container_width 사용)
            st.image(result_img, caption="짜잔! 서재페 프사 완성! 🎷", use_container_width=True)

            # 다운로드 버튼 생성 (투명 배경 유지를 위해 PNG로 저장)
            buf = io.BytesIO()
            result_img.save(buf, format="PNG")
            st.download_button(
                label="📥 NEW 프사 다운로드 (PNG)",
                data=buf.getvalue(),
                file_name="sjf_profile_circle.png",
                mime="image/png"
            )
