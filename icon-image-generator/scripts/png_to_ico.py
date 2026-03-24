from pathlib import Path
import sys

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit(
        "缺少 Pillow 依赖，请先执行: pip install pillow"
    ) from exc

SIZES = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python png_to_ico.py <input.png> [output.ico]")
        return 1

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(f"输入文件不存在: {input_path}")
        return 1

    if input_path.suffix.lower() != ".png":
        print("输入文件必须是 PNG 格式")
        return 1

    output_path = (
        Path(sys.argv[2]).expanduser().resolve()
        if len(sys.argv) >= 3
        else input_path.with_suffix(".ico")
    )

    with Image.open(input_path) as img:
        img = img.convert("RGBA")
        img.save(output_path, format="ICO", sizes=SIZES)

    print(f"ICO 已生成: {output_path}")
    print("包含尺寸: 256, 128, 64, 48, 32, 16")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
