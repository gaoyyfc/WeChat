"""Export proportional publication copies and contact sheets without image edits."""

import json
from pathlib import Path
import re
import zipfile

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUTPUTS = REPO / "outputs"


def main():
    topics = json.loads((HERE / "选题制作清单.json").read_text())
    covers = []
    all_files = []
    manifest = []
    for topic in topics:
        folder = HERE / topic["slug"]
        data = json.loads((folder / "制作内容.json").read_text())
        base = OUTPUTS / topic["folder"]
        out = base / "公众号贴图"
        out.mkdir(parents=True, exist_ok=True)
        review = folder / "review"
        cards, dimensions = [], []
        for i, card_spec in enumerate(data["cards"]):
            source = folder / "generated" / (card_spec["id"] + ".png")
            with Image.open(source) as original:
                original.load()
                if original.width * 4 != original.height * 3:
                    raise ValueError(f"{source}: original is not 3:4")
                card = original.convert("RGB").resize((1080, 1440), Image.Resampling.LANCZOS)
                dest = out / (card_spec["output"] + ".png")
                card.save(dest, optimize=True)
                dimensions.append({"file": dest.name, "size": [1080, 1440], "source": source.name, "source_size": list(original.size)})
            with Image.open(dest) as exported:
                exported.load()
                assert exported.size == (1080, 1440) and exported.format == "PNG"
            cards.append(card)
            all_files.append(dest)
            card.resize((360, 480), Image.Resampling.LANCZOS).save(review / f"手机宽度-{i+1:02d}.jpg", quality=96)
        covers.append(cards[0])
        rows = (len(cards) + 1) // 2
        spread = Image.new("RGB", (1080, 720 * rows), "#F8F7F3")
        for i, card in enumerate(cards):
            spread.paste(card.resize((540, 720), Image.Resampling.LANCZOS), ((i % 2) * 540, (i // 2) * 720))
        spread.save(review / "整组贴图预览.jpg", quality=94)
        (review / "发布图片尺寸.json").write_text(json.dumps(dimensions, ensure_ascii=False, indent=2) + "\n")
        package = base / (topic["folder"].replace("-20261111", "") + "-公众号贴图发布包.zip")
        with zipfile.ZipFile(package, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(out.iterdir()):
                if path.is_file():
                    archive.write(path, arcname="公众号贴图/" + path.name)
                    if path not in all_files:
                        all_files.append(path)
        with zipfile.ZipFile(package) as archive:
            assert archive.testzip() is None
            assert len(archive.namelist()) == len(cards) + 4
        manifest.append({"title": topic["title"], "images": len(cards), "package": str(package.relative_to(REPO)), "checks": "passed"})
        print(f"EXPORTED {topic['slug']}: {len(cards)} PNGs, 1080x1440, ZIP verified", flush=True)

    summary = Image.new("RGB", (1620, 720), "#F8F7F3")
    for i, cover in enumerate(covers):
        summary.paste(cover.resize((540, 720), Image.Resampling.LANCZOS), (i * 540, 0))
    (HERE / "review").mkdir(exist_ok=True)
    summary.save(HERE / "review/三组封面对照.jpg", quality=95)
    combined_out = OUTPUTS / "中年生活三组贴图-20261111"
    combined_out.mkdir(exist_ok=True)
    combined_zip = combined_out / "三组贴图与发布配文-共19张.zip"
    with zipfile.ZipFile(combined_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in all_files:
            archive.write(path, arcname=str(path.relative_to(OUTPUTS)))
    with zipfile.ZipFile(combined_zip) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == 31

    for path in HERE.rglob("*"):
        if path.suffix.lower() in {".md", ".txt", ".py", ".json"}:
            content = path.read_text()
            if re.search(r"sk-[A-Za-z0-9_-]{20,}", content):
                raise ValueError(f"Potential credential in {path.name}")
    for path in all_files:
        if path.suffix in {".md", ".txt"}:
            assert "**" not in path.read_text()
    (HERE / "review/文件验证.json").write_text(json.dumps({"topics": manifest, "total_images": 19, "total_zip_entries": 31, "credentials_scan": "passed", "zip_integrity": "passed"}, ensure_ascii=False, indent=2) + "\n")
    print("ALL CHECKS PASSED: 19 publication images and 3 complete copy sets.")


if __name__ == "__main__":
    main()
