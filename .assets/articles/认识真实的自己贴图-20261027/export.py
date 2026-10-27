"""等比导出发布图、拼接审阅图；不叠字或修改画面内容。"""

from pathlib import Path
import json
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[2] / 'outputs/认识真实的自己-20261027/公众号贴图'
MAPPING = [
    ('01-cover', '01-封面'),
    ('02-labels', '02-少贴标签'),
    ('03-strengths', '03-找到长处'),
    ('04-energy', '04-看清消耗'),
    ('05-priorities', '05-排出选择'),
    ('06-card', '06-我的使用说明'),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    review = HERE / 'review'
    review.mkdir(exist_ok=True)
    cards = []
    records = []
    for source_name, output_name in MAPPING:
        with Image.open(HERE / 'generated' / f'{source_name}.png') as im:
            im.load()
            if im.width * 4 != im.height * 3:
                raise ValueError(f'{source_name}: 原图不是3:4，停止导出')
            card = im.convert('RGB').resize((1080, 1440), Image.Resampling.LANCZOS)
            card.save(OUT / f'{output_name}.png', optimize=True)
            cards.append(card)
            records.append({
                'file': f'{output_name}.png',
                'width': 1080,
                'height': 1440,
                'source': f'{source_name}.png',
                'source_size': list(im.size),
            })

    # 两列三排，完整保留各图，不加文字、边框或其他装饰。
    spread = Image.new('RGB', (1080, 2160), 'white')
    for i, card in enumerate(cards):
        spread.paste(
            card.resize((540, 720), Image.Resampling.LANCZOS),
            ((i % 2) * 540, (i // 2) * 720),
        )
        card.resize((360, 480), Image.Resampling.LANCZOS).save(
            review / f'手机宽度-{i+1:02d}.jpg', quality=96
        )
    spread.save(review / '六张贴图总览.jpg', quality=94)
    (review / '发布图片尺寸.json').write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + '\n'
    )
    print(json.dumps({'exported': len(records), 'size': '1080x1440'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
