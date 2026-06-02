from PIL import Image, ImageDraw, ImageFilter

def make_icon(S, maskable=False):
    img = Image.new('RGBA', (S, S), (11, 18, 48, 255))
    d = ImageDraw.Draw(img)
    # 밤하늘 그라데이션 (16,24,60) -> (8,13,34)
    for y in range(S):
        t = y / S
        d.line([(0, y), (S, y)], fill=(int(16-8*t), int(24-11*t), int(60-26*t), 255))
    pad = int(S*0.12) if maskable else 0
    inner = S - 2*pad
    sx = lambda x: pad + x*inner/512
    sy = lambda y: pad + y*inner/512
    # 달빛 글로우
    glow = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    mx, my, mr = sx(355), sy(155), inner*0.085
    gd.ellipse([mx-mr*3, my-mr*3, mx+mr*3, my+mr*3], fill=(244, 214, 138, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(S*0.035))
    img = Image.alpha_composite(img, glow)
    d = ImageDraw.Draw(img)
    # 별
    for (x, y) in [(80,90),(150,55),(235,105),(120,185),(300,70),(430,115),(455,205),(60,250),(390,165)]:
        px, py = sx(x), sy(y)
        rr = max(inner*0.007, 1)
        d.ellipse([px-rr, py-rr, px+rr, py+rr], fill=(230, 236, 255, 255))
    # 달
    d.ellipse([mx-mr, my-mr, mx+mr, my+mr], fill=(245, 224, 152, 255))
    # 산 능선
    d.polygon([(sx(-10), sy(430)), (sx(175), sy(255)), (sx(335), sy(430))], fill=(47, 107, 65, 255))
    d.polygon([(sx(245), sy(430)), (sx(400), sy(235)), (sx(565), sy(430))], fill=(22, 51, 31, 255))
    d.rectangle([sx(-5), sy(425), sx(517), sy(517)], fill=(12, 40, 28, 255))
    return img.convert('RGB')

base = make_icon(512)
base.save('icon-512.png')
base.resize((192, 192), Image.LANCZOS).save('icon-192.png')
base.resize((180, 180), Image.LANCZOS).save('apple-touch-icon.png')
make_icon(512, maskable=True).save('icon-512-maskable.png')
print('icons created: icon-512.png, icon-192.png, apple-touch-icon.png, icon-512-maskable.png')
