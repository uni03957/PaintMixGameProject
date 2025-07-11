import streamlit as st
import numpy as np
import colorVisualize as cv
import logistic as lg

# LUT 캐싱, 256바이트 크기로 효율적인 캐시
@st.cache_data
def buildLUT(cdf, size=256) -> np.ndarray:
    """빠른 탐색을 위한 LUT 테이블을 생성하는 함수."""
    # 256바이트의 작은 numpy 배열 룩업테이블을 통해 빠른 탐색.
    # 정적인 룩업테이블이고, 모바일 경량화를 위해 256바이트만큼 메모리에 유지.
    # CDF의 비율에 맞게 색상 인덱스를 저장함.
    lut = np.zeros(size, dtype=np.uint8)
    
    # 0~1까지를 256단계로 나눈 임의 값.
    # CDF의 임계점과 비교해 룩업테이블을 완성.
    values = np.linspace(0,1,256)

    # 0~6까지의 인덱스는 색상(빨강, 초록, 파랑, 마젠타, 노랑, 시안, 블랙). 기본 값은 0으로 설정.
    lut = np.searchsorted(cdf, values, side='left').astype(np.uint8)
    return lut

# 색상 비율과 CDF.
# 인덱스 순서: Red, Green, Blue, Magenta, Yellow, Cyan, Black.
COLOR_RATIOS = [0.25, 0.25, 0.25, 0.08, 0.08, 0.08, 0.01]
cdf = np.cumsum(COLOR_RATIOS)

st.sidebar.title("물감 랜덤 생성 입력값")

x0 = st.slider("시드 값", min_value=0.35, max_value=0.48, value=0.35, step=0.001)
r = st.slider("로지스틱 파라미터 r", min_value=3.7, max_value=4.0, value=3.7, step=0.01)



imageBuf = None



if st.button("시뮬레이션 실행"):
    logSequence = lg.logisticMapList(r,x0)
    lutSequence = lg.mappingLUT(logSequence, buildLUT(cdf))
    fig = cv.createColorGridFigure(lutSequence, r, x0)
    cv.renderColorGrid(fig)
    imageBuf = cv.saveImage(fig)

    
st.write(f"선택된 시드: {x0}, 선택된 파라미터 r: {r}")


if imageBuf:
    st.download_button(
        
        label="이미지 다운로드",
        data=imageBuf,
        file_name=f"color_grid_x0_{x0}_r_{r}.png",
        mime="image/png"
    )

