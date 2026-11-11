"""等比导出发布图与审阅图，不叠字、不改动生成画面内容。"""
from pathlib import Path
import json
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / "outputs/别人说话让你不舒服-20261111/公众号贴图"

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    review = HERE / "review"
    review.mkdir(exist_ok=True)
    data = json.loads((HERE / "制作内容.json").read_text())
    cards, records = [], []
    for item in data["cards"]:
        source = HERE / "generated" / (item["id"] + ".png")
        with Image.open(source) as im:
            im.load()
            if im.width * 4 != im.height * 3:
                raise ValueError(f"{source.name}: 原图不是3:4")
            card = im.convert("RGB").resize((1080,1440), Image.Resampling.LANCZOS)
            dest = OUT / (item["output"] + ".png")
            card.save(dest, optimize=True)
            cards.append(card)
            records.append({"file":dest.name,"size":[1080,1440],"source":source.name,"source_size":list(im.size)})
    spread = Image.new("RGB", (1080,2880), "#FAFAF7")
    for i, card in enumerate(cards):
        spread.paste(card.resize((540,720), Image.Resampling.LANCZOS), ((i%2)*540,(i//2)*720))
        card.resize((360,480), Image.Resampling.LANCZOS).save(review / f"手机宽度-{i+1:02d}.jpg",quality=96)
    spread.save(review / "七张贴图总览.jpg",quality=94)
    (review / "发布图片尺寸.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"exported":len(records),"size":"1080x1440"},ensure_ascii=False))

if __name__ == "__main__":
    main()
