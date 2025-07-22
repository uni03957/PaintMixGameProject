using UnityEngine;

namespace PaintGame
{
    /// <summary> 바이트 컬러 매핑  /// </summary>
    public enum PaintColor : byte
    {
        Done = 0b000,
        Magenta = 0b001,
        Yellow = 0b010,
        Cyan = 0b100,
        Red = 0b011,
        Blue = 0b101,
        Green = 0b110,
        Black = 0b111
    }

    public static class ColorMapper
    {
        /// <summary>
        /// 빠르게 컬러에 매핑하기 위한 LUT
        /// </summary>
        private static readonly Color[] ColorLUT = new Color[8]
        {
            Color.white, //완료
            Color.magenta,
            Color.yellow,
            Color.cyan,
            Color.red,
            Color.blue,
            Color.green,
            Color.black
        };

        /// <summary>
        /// byte 타입 파라미터를 PaintColor로 매핑하고, LUT 테이블로 반환하는 함수.
        /// </summary>
        /// <param name="code"> byte 타입이고, XXXX X000 중 0의 값들로 매핑. </param>
        /// <returns>Color로 나옴.</returns>
        public static Color FromPaintColor(PaintColor code)
        {
            return ColorLUT[(int)code];
        }
    }
}