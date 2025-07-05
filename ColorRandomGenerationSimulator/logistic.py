import numpy as np

def logisticMapList(r: float, x0: float) -> list[float]:
    # 시드로 로지스틱 맵을 200번 계산해서, 수열 리스트로 저장 후 반환.
    x = x0
    sequence = []
    for i in range(128):
        x = r * x * (1-x)
        sequence.append(x)
    return sequence

def mappingLUT(sequence: list[float], lut:np.array) -> list[int]:
    # 0~1값을 나눠 저장한 LUT에 기반하여, 컬러 인덱스와 매핑.
    colorSequence=[]

    for value in sequence:
        # 256단계로 양자화 - ChatGPT
        lutIndex = int(value * 255)
        # 0~255 범위로 안전하게 제한 - ChatGPT
        lutIndex = min(max(lutIndex, 0),255) 
        colorSequence.append(lut[lutIndex])

    return colorSequence
