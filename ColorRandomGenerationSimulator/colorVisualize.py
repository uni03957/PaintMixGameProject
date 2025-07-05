import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import analysis as an
from io import BytesIO
from matplotlib.patches import Rectangle
from matplotlib.figure import Figure


COLOR_MAP = np.array([
    [255, 0, 0],     # Red
    [0, 255, 0],     # Green
    [0, 0, 255],     # Blue
    [255, 0, 255],   # Magenta
    [255, 255, 0],   # Yellow
    [0, 255, 255],   # Cyan
    [0, 0, 0]        # Black
], dtype=np.uint8)

COLOR_LABEL = ['Red', 'Green', 'Blue', 'Magenta', 'Yellow', 'Cyan', 'Black']

COLOR_CODES = ['r', 'g', 'b', 'm', 'y', 'c', 'k']

# ChatGPT가 알려준 사각화 방식
def createColorGridFigure(colorSequence: np.ndarray, r, x0, shape = (8,16), layoutLength=2, layoutWidth=2) -> Figure:
    """2차원 배열을 사각형 타일화하고, 타일로 시각화된 이미지와 통계 그래프를 subplot으로 만드는 함수."""
    colorArray = COLOR_MAP[colorSequence].reshape(shape[0], shape[1], 3)
    
    # RGB 값 제외 가져와 행과 열로 사용
    rows, cols = colorArray.shape[:2]

    colorCount = an.colorCounter(colorSequence)
    colorConnectedComponent = an.connectedComponent(colorSequence.reshape(shape[0], shape[1]))

    """
    [디버깅]
    for i,j in colorConnectedComponent.items():
        print(f"{j[0]}: 군집 수: {j[1]}, 평균 연결 개수: {j[2]}, 최대 연결 개수: {j[3]}")
    """

    fig, axs= plt.subplots(layoutLength, layoutWidth, figsize=(14, 6))
    ax1, ax2, ax3, ax4 = axs.flat

    for i in range(rows):
        for j in range(cols):
            rgb = tuple(colorArray[i, j] / 255.0)  # matplotlib: 색상값 0~1 정규화
            rect = Rectangle((j, rows - i - 1), 1, 1, facecolor=rgb) # matplotlib은 아래에서 위로 인덱싱하는 구조라 반대로.
            ax1.add_patch(rect)
    # 제목 또는 정보 텍스트 삽입
    ax1.set_title(f"Color Grid (x₀ = {x0}, r = {r})")

    # 랜덤 생성된 타일 시각화
    ax1.set_xlim(0, cols)
    ax1.set_ylim(0, rows)
    ax1.set_aspect('equal')
    ax1.axis('off')

    # 색상 수 그래프
    x = np.arange(7)
    ax2.bar(x, colorCount, color=COLOR_CODES)
    ax2.set_xticks(x, COLOR_LABEL)
    ax2.set_title("Color Distribution")
    ax2.set_xlabel("Color")
    ax2.set_ylabel("Count")
    
    # 군집 수 그래프
    group_counts = [info[1] for info in colorConnectedComponent.values()]
    ax3.bar(x, group_counts, color=COLOR_CODES)
    ax3.set_xticks(x, COLOR_LABEL)
    ax3.set_title("Connected Components")

    # 평균 연결 개수와 최대 연결 개수 그래프
    avg_sizes = [info[2] for info in colorConnectedComponent.values()]
    max_sizes = [info[3] for info in colorConnectedComponent.values()]

    ax4.bar(x, avg_sizes, color=COLOR_CODES, label='Average Connected Color Count')
    ax4.plot(x, max_sizes, color='black', linestyle='--', marker='o', linewidth=2, label='Max Connected Color Count')

    ax4.set_xticks(x, COLOR_LABEL)
    ax4.set_title("Average vs Max Cluster Size")
    ax4.set_xlabel("Color")
    ax4.set_ylabel("Connected Tiles")
    ax4.legend()

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
