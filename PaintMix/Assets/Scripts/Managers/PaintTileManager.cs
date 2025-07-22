using System.Collections.Generic;
using UnityEngine;
using PaintGame;
using Unity.VisualScripting.FullSerializer;
using Unity.VisualScripting;

namespace PaintGame
{
    /// <summary>
    /// PaintTile을 그리드로 생성하고 초기화하는 매니저
    /// </summary>
    public class PaintTileManager : MonoBehaviour
    {
        // -- 필드 --
        [Header("Grid Settings")]
        [SerializeField] private int columns = 16;
        [SerializeField] private int rows = 8;
        Color[,] colorMap;
        PaintTile[,] tileMap;

        [Header("References")]
        [SerializeField] private GameObject tilePrefab;
        [SerializeField] private Transform tileParent;

        // -- 시작 --
        private void Start()
        {
            colorMap = new Color[rows, columns];
            tileMap = new PaintTile[rows, columns];


            GenerateGrid();
        }

        // -- 메서드 --
        /// <summary>
        /// 그리드에 타일을 생성하고 초기화함.
        /// </summary>
        private void GenerateGrid()
        {
            // 행 -> 열 순서로 메모리 캐시를 유지하며 초기화
            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < columns; c++)
                {
                    GameObject tileGameObject = Instantiate(tilePrefab, tileParent);

                    if (tileGameObject.TryGetComponent<PaintTile>(out var tile))
                    {
                        tile.Init(c, r);
                
                        tileMap[r, c] = tile;
                        
                        //임시 랜덤 생성 코드
                        PaintColor[] values = (PaintColor[])System.Enum.GetValues(typeof(PaintColor));
                        PaintColor randomColor = values[Random.Range(0, values.Length)];
                        tile.SetColor((byte)randomColor);

                        colorMap[r, c] = tile.TileColor;
                        Debug.Log($"({r},{c}): color: {colorMap[r, c]}, {tileMap[r, c]}");
                    }
                    else
                    {
                        Debug.LogWarning("타일 Prefab에 PaintTile 컴포넌트가 없습니다.", tileGameObject);
                    }
                }
            }
        }
    }
}
