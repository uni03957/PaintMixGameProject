import numpy as np
from collections import Counter

def colorCounter(colorSequence: np.ndarray) -> list[int]:
    # 색상 수 세기
    countDict = Counter(colorSequence)
    return [countDict.get(i, 0) for i in range(7)]


def connectedComponent(colorArray: np.ndarray, minClusterCount=2) -> dict:
    # ChatGPT가 제안한 방문 배열 생성을 통해 조건 검토
    visited = np.zeros_like(colorArray, dtype=bool)
    direction = [
                (-1,1), (0,1), (1,1),
                (-1,0),        (1,0),
                (-1,-1), (0,-1), (1,-1)
            ]
    # colorArray를 계속 인자로 받지 않고 재활용
    # DFS 탐색 구조를 활용해 2차원 배열을 그래프 형태로 고려
    def checkCountAdjacentSameColorTile(tileColor: int, index: tuple) -> int:
        stack = [index]
        visited[index[0], index[1]] = True
        count = 1
        
        while stack:
            i, j = stack.pop()
            for dx, dy in direction:
                ni, nj = i + dx, j + dy
                if 0 <= ni < colorArray.shape[0] and 0 <= nj < colorArray.shape[1]:
                    if not visited[ni, nj] and colorArray[ni, nj] == tileColor:
                        visited[ni, nj] = True
                        # 탐색 후보 추가
                        stack.append((ni, nj))
                        count += 1
        return count
    
    # ChatGPT가 제안한 색상 확장 가능한 딕셔너리 생성
    COLOR_NAMES = ["Red", "Green", "Blue", "Magenta", "Yellow", "Cyan", "Black"]
    # 구조: [ColorName, 군집 수, 군집 평균 크기, 군집 최대 크기]
    colorConnectedComponent = {i: [name, 0, 0, 0] for i, name in enumerate(COLOR_NAMES)}


    for (i,j), color in np.ndenumerate(colorArray):
        if not visited[i, j]:
            group_size = checkCountAdjacentSameColorTile(color, (i, j))
            if group_size >= minClusterCount:
                colorConnectedComponent[color][1] += 1 
                colorConnectedComponent[color][2] += group_size
                colorConnectedComponent[color][3] = max(colorConnectedComponent[color][3], group_size)

    for k in colorConnectedComponent:
        group_count = colorConnectedComponent[k][1]
        if group_count:
            colorConnectedComponent[k][2] /= group_count

    return colorConnectedComponent

