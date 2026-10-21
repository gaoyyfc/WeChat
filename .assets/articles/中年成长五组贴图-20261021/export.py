"""机械缩放已验收原图，生成发布文件与审阅拼图；不修改图中文字。"""

import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
data = json.loads((HERE / "制作内容.json").read_text())
sources = [
    HERE / "generated" / f"{group['id']}-{page['file']}.png"
    for group in data["series"] for page in group["pages"]
]
missing = [path.name for path in sources if not path.exists()]
if missing:
    raise SystemExit("未完成原图：" + ", ".join(missing))

records = []
covers = []
for group in data["series"]:
    output = REPO / "outputs" / group["directory"] / "公众号贴图"
    output.mkdir(parents=True, exist_ok=True)
    page_previews = []
    for page in group["pages"]:
        source = HERE / "generated" / f"{group['id']}-{page['file']}.png"
        with Image.open(source) as image:
            if image.width * 4 != image.height * 3:
                raise SystemExit("原图比例异常：" + source.name)
            final = image.convert("RGB").resize((1080, 1440), Image.Resampling.LANCZOS)
            dest = output / f"{page['file']}.png"
            final.save(dest)
            records.append({"path": str(dest.relative_to(REPO)), "width": 1080, "height": 1440})
            page_previews.append(final.resize((540, 720), Image.Resampling.LANCZOS))
            if page["file"] == "01-cover":
                covers.append(final.resize((360, 480), Image.Resampling.LANCZOS))
    contact = Image.new("RGB", (1620, 720), "#faf7ef")
    for i, preview in enumerate(page_previews):
        contact.paste(preview, (i * 540, 0))
    contact.save(HERE / "review" / f"{group['id']}.jpg", quality=92)

overview = Image.new("RGB", (1080, 960), "#faf7ef")
for preview, position in zip(covers, [(0, 0), (360, 0), (720, 0), (180, 480), (540, 480)]):
    overview.paste(preview, position)
overview.save(HERE / "review" / "五组封面总览.jpg", quality=94)
(HERE / "review" / "发布图片尺寸.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
print(f"发布图 {len(records)} 张，全部为 1080×1440；保存了五组审阅拼图与封面总览。")
