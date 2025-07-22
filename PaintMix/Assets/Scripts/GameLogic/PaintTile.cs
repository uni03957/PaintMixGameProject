using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

namespace PaintGame
{
    [RequireComponent(typeof(Image))]
    public class PaintTile : MonoBehaviour
    {
        // -- 프로퍼티 --
        /// <summary> 타일의 좌표 (읽기 전용) </summary>
        public Vector2Int Position { get; private set; }

        /// <summary> 현재 타일 색상 </summary>
        public Color TileColor => TileImage.color;

        /// <summary> 선택 상태 </summary>
        public bool IsSelected { get; private set; }

        

        // -- 컴포넌트 --
        private Image _tileImage;

        //null 일 때만 할당하는 Lazy-Load 기법 - ChatGPT가 제안함.
        private Image TileImage => _tileImage ??= GetComponent<Image>();




        // -- 메서드 --
        /// <summary> 타일 초기화 및 좌표 설정 </summary>
        public void Init(int x, int y)
        {
            Position = new Vector2Int(x, y);
            
            name = $"Tile ({x},{y})";
        }

        /// <summary> 타일 색상 설정 </summary>
        public void SetColor(byte infoCode)
        {
            TileImage.color = ColorMapper.FromPaintColor((PaintColor)infoCode);
        }

        /// <summary> 타일이 선택됐을 시 (확장 필요)</summary>
        public void Select(Color highlightColor)
        {
            IsSelected = true;
            TileImage.color = highlightColor;
        }

        /// <summary> 타일 선택이 해제됐을 시 </summary>
        public void Deselect()
        {
            IsSelected = false;
        }
    }
}

