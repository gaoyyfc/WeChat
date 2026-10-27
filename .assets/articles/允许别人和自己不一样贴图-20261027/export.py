"""等比导出发布图并拼接审阅图；不叠字、不修改原图内容。"""

from pathlib import Path
import json
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / "outputs/允许别人和自己不一样-20261027/公众号贴图"
MAPPING = [
    ("01-cover", "01-封面"),
    ("02-work", "02-同事意见不同"),
    ("03-choice", "03-亲友不理解"),
    ("04-boundary", "04-守住边界"),
    ("05-practice", "05-三行整理卡"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    review = HERE / "review"
    review.mkdir(exist_ok=True)
    records = []
    cards = []
    for source_name, output_name in MAPPING:
        with Image.open(HERE / "generated" / f"{source_name}.png") as source:
            source.load()
            if source.width * 4 != source.height * 3:
                raise ValueError(f"{source_name}: 原图不符合3:4，停止导出")
            exported = source.convert("RGB").resize(
                (1080, 1440), Image.Resampling.LANCZOS
            )
            exported.save(OUT / f"{output_name}.png", optimize=True)
            records.append({
                "file": f"{output_name}.png",
                "width": 1080,
                "height": 1440,
                "source": f"{source_name}.png",
                "source_size": list(source.size),
            })
            cards.append(exported)

    # 保留每张完整画面，前两张在上排，后三张在下排。
    spread = Image.new("RGB", (1080, 1200), "white")
    for i, card in enumerate(cards[:2]):
        spread.paste(card.resize((540, 720), Image.Resampling.LANCZOS), (i * 540, 0))
    for i, card in enumerate(cards[2:]):
        spread.paste(card.resize((360, 480), Image.Resampling.LANCZOS), (i * 360, 720))
    spread.save(review / "五张贴图总览.jpg", quality=94)

    # 全部五张都提供360px宽审阅版，不加边框、编号或其他文字。
    for i, card in enumerate(cards):
        card.resize((360, 480), Image.Resampling.LANCZOS).save(
            review / f"手机宽度-{i + 1:02d}.jpg", quality=96
        )
    (review / "发布图片尺寸.json").write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({"exported": len(records), "size": "1080x1440"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
