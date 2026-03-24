from pathlib import Path
import sys

try:
    from rembg import remove
except ImportError as exc:
    raise SystemExit(
        "缺少 rembg 依赖，请先执行: pip install rembg"
    ) from exc


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python remove_bg.py <input.png> [output.png]")
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
        else input_path.with_name(f"{input_path.stem}_transparent.png")
    )

    data = input_path.read_bytes()
    result = remove(data)
    output_path.write_bytes(result)

    print(f"透明背景 PNG 已生成: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
