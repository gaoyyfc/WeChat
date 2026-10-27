"""等比缩放发布图、生成审阅拼图；不叠字、不修改原图内容。"""
from pathlib import Path
import json
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent
OUT=HERE.parents[2]/'outputs/31省份平均工资出炉-20261027/公众号贴图'
MAPPING=[('01-cover','01-封面'),('02-facts','02-先看统计对象'),('03-average','03-平均数不是多数人'),('04-paycheck','04-税前与到手'),('05-action','05-薪资核对卡')]
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    review=HERE/'review';review.mkdir(exist_ok=True)
    rows=[];cards=[]
    for src,dest in MAPPING:
        with Image.open(HERE/'generated'/f'{src}.png') as im:
            assert im.width*4==im.height*3,(src,im.size)
            exported=im.convert('RGB').resize((1080,1440),Image.Resampling.LANCZOS)
            exported.save(OUT/f'{dest}.png',optimize=True)
            rows.append({'file':dest+'.png','width':1080,'height':1440,'source':src+'.png','source_size':list(im.size)})
            cards.append(exported.resize((540,720),Image.Resampling.LANCZOS))
    # 拼图保持每张全部画面，没有裁切、加字或装饰
    spread=Image.new('RGB',(1080,1200),'white')
    for i,card in enumerate(cards[:2]):spread.paste(card,(i*540,0))
    for i,card in enumerate(cards[2:]):
        spread.paste(card.resize((360,480),Image.Resampling.LANCZOS),(i*360,720))
    spread.save(review/'五张贴图总览.jpg',quality=94)
    # 手机宽度检查：两张封面/数据页原图仅缩放后并排，字号与360px手机接近
    phone=Image.new('RGB',(720,480),'white')
    for i,card in enumerate(cards[:2]):phone.paste(card.resize((360,480),Image.Resampling.LANCZOS),(360*i,0))
    phone.save(review/'手机宽度检查.jpg',quality=96)
    (review/'发布图片尺寸.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'exported':len(rows),'size':'1080x1440'},ensure_ascii=False))
if __name__=='__main__':main()
