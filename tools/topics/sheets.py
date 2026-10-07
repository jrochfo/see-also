import json, re, io, urllib.request, sys, os, textwrap, time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont
D=os.path.dirname(os.path.abspath(__file__))
S=json.load(open(sys.argv[1]))
OUT=os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])),'sheets'); os.makedirs(OUT,exist_ok=True)
UA={'User-Agent':'SeeAlso-dev (jake.rochford@gmail.com)'}
try: F=ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',13)
except Exception: F=ImageFont.load_default()
def get(u):
    u=u.split('?')[0]; small=re.sub(r'/\d+px-','/250px-',u)
    for url in (small,u):
        for i in range(2):
            try:
                b=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=30).read()
                im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((220,160)); return im
            except Exception: time.sleep(1)
    return None
W,H,C=230,215,6
for key,items in S.items():
    if not items: continue
    with ThreadPoolExecutor(4) as ex: ims=list(ex.map(lambda i:get(i['img']),items))
    rows=(len(items)+C-1)//C; sheet=Image.new('RGB',(W*C,H*rows+30),'white'); d=ImageDraw.Draw(sheet)
    d.text((8,8),key,fill='black',font=F)
    for n,(it,im) in enumerate(zip(items,ims)):
        x=(n%C)*W+5; y=(n//C)*H+30
        if im: sheet.paste(im,(x,y))
        d.text((x,y+163),f"{n+1}. "+'\n'.join(textwrap.wrap(it['caption'],34)[:2]),fill='black',font=F)
        d.text((x,y+193),textwrap.shorten(it['title'],34),fill='#3366cc',font=F)
    sheet.save(f'{OUT}/sheet-{key}.png')
    print('sheet',key,flush=True)
