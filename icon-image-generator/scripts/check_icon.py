from pathlib import Path
import sys

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit(
        "缺少 Pillow 依赖，请先执行: pip install pillow"
    ) from exc

MIN_SIZE = 512
RECOMMENDED_SIZE = 1024


def has_transparency(img: Image.Image) -> bool:
    if img.mode in ("RGBA", "LA"):
        alpha = img.getchannel("A")
        return alpha.getbbox() is not None
    if img.mode == "P" and "transparency" in img.info:
        return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python check_icon.py <input.png>")
        return 1

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(f"输入文件不存在: {input_path}")
        return 1

    if input_path.suffix.lower() != ".png":
        print("输入文件必须是 PNG 格式")
        return 1

    with Image.open(input_path) as img:
        width, height = img.size
        square = width == height
        transparent = has_transparency(img)

    print(f"文件: {input_path}")
    print(f"尺寸: {width}x{height}")
    print(f"是否正方形: {'是' if square else '否'}")
    print(f"是否存在透明通道: {'是' if transparent else '否'}")

    issues = []
    suggestions = []

    if not square:
        issues.append("源图不是正方形，不适合直接作为标准 Windows 图标主图")

    if width < MIN_SIZE or height < MIN_SIZE:
        issues.append(f"分辨率低于 {MIN_SIZE}x{MIN_SIZE}，缩放后容易发糊")
    elif width < RECOMMENDED_SIZE or height < RECOMMENDED_SIZE:
        suggestions.append(f"建议使用至少 {RECOMMENDED_SIZE}x{RECOMMENDED_SIZE} 的源图，以获得更好的 ico 缩放质量")

    if not transparent:
        suggestions.append("建议使用透明背景，否则在不同主题或桌面背景下兼容性较差")

    if issues:
        print("\n问题:")
        for item in issues:
            print(f"- {item}")
    else:
        print("\n问题:")
        print("- 未发现阻止转换的明显问题")

    if suggestions:
        print("\n建议:")
        for item in suggestions:
            print(f"- {item}")

    return 0 if not issues else 2


if __name__ == "__main__":
    raise SystemExit(main())
