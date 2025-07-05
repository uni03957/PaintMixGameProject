import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.patches import Rectangle
from matplotlib.figure import Figure
from collections import Counter

COLOR_MAP = {
    0: (255, 0, 0), # Red
    1: (0, 255, 0), # Green 
    2: (0, 0, 255), # Blue
    3: (255, 0, 255), # Magenta
    4: (255, 255, 0), # Yellow
    5: (0, 255, 255), # Cyan
    6: (0, 0, 0) # Black
}

def toColorGrid(colorSequence: list[int], shape=(8, 16)) -> np.ndarray:
    """RGB 값을 지닌 2차원 배열로 만드는 함수."""
    colorArray = []
    for index in colorSequence:
        colorArray.append(COLOR_MAP[index])
    # RGB 2차원 배열로 변환
    colorArray = np.array(colorArray, dtype=np.uint8).reshape(shape[0], shape[1], 3) 

    return colorArray


# ChatGPT가 알려준 사각화 방식
def createColorGridFigure(colorArray: np.ndarray, colorSequence: list[int], r, x0) -> Figure:
    """2차원 배열을 사각형 타일화하고, 타일로 시각화된 이미지와 통계 그래프를 subplot으로 만드는 함수."""
    # RGB 값 제외 가져와 행과 열로 사용
    rows, cols = colorArray.shape[:2]

    # 색상 수 세기
    countDict = Counter(colorSequence)
    colorCount = [countDict.get(i, 0) for i in range(7)]

    
    fig, (ax1, ax2)= plt.subplots(1, 2, figsize=(10, 6))

    for i in range(rows):
        for j in range(cols):
            rgb = tuple(colorArray[i, j] / 255.0)  # matplotlib: 색상값 0~1 정규화
            rect = Rectangle((j, rows - i - 1), 1, 1, facecolor=rgb) # matplotlib은 아래에서 위로 인덱싱하는 구조라 반대로.
            ax1.add_patch(rect)
    # 제목 또는 정보 텍스트 삽입
    ax1.set_title(f"Color Grid (x₀ = {x0}, r = {r})")

    ax1.set_xlim(0, cols)
    ax1.set_ylim(0, rows)
    ax1.set_aspect('equal')
    ax1.axis('off')

    COLOR_LABEL = ['Red', 'Green', 'Blue', 'Magenta', 'Yellow', 'Cyan', 'Black']
    COLOR_CODES = ['r', 'g', 'b', 'm', 'y', 'c', 'k']

    x = np.arange(7)
    ax2.bar(x, colorCount, color=COLOR_CODES)
    ax2.set_xticks(x, COLOR_LABEL)
    ax2.set_title("Color Distribution")
    ax2.set_xlabel("Color")
    ax2.set_ylabel("Count")

    plt.tight_layout()
    return fig



def renderColorGrid(fig):
    """해당 subplot을 표시하는 함수."""
    st.pyplot(fig)

def saveImage(fig):
    """해당 subplot을 이미지 저장을 위해 버퍼에 담는 함수."""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)

    return buf
