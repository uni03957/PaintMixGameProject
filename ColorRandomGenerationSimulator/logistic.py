import numpy as np

def logisticMapList(r: float, x0: float, count = 128, burnInNum = 20) -> np.ndarray:
    """시드 x0으로 파라미터 r에 기반한 로지스틱 사상을 계산 후, 초반 수렴 구간을 제외하고, 결과 리스트를 계산하여 반환하는 함수."""
    # 시드로 로지스틱 맵을 계산해서, 수열 리스트로 저장 후 반환.
    x = x0

    # ChatGPT가 제안한 초반 수렴 구간 제외하고 반영.
    for i in range(burnInNum):
        x = r * x * (1 - x)

    sequence = np.empty(count, dtype=np.float64)
    for i in range(count):
        x = r * x * (1-x)
        sequence[i] = x
    return sequence

def mappingLUT(sequence: np.ndarray, lut:np.ndarray) -> np.ndarray:
    """로지스틱 사상의 결과로 0~1의 값을 지닌 요소들의 리스트를 받아 0~6의 컬러 인덱스로 매핑하는 함수. 
    0: Red, 1: Green, 2: Blue, 3: Magenta, 4: Yellow, 5: Cyan, 6: Black.
    """
    # 0~1값을 나눠 저장한 LUT에 기반하여, 컬러 인덱스와 매핑.

    # sequence 양자화하여 0 ~ 255 값 인덱스로 변경
    colorIndices = np.clip((sequence * 255).astype(int), 0, 255)

    # 벡터화 인덱싱
    return lut[colorIndices] 
