from PIL import Image, ImageEnhance
import numpy as np

BRAND = np.array([11., 18., 20.])   # #0B1214

def grade(img, sat=0.60, bright=0.78, tone=0.22, warm=1.06):
    im = ImageEnhance.Color(img).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    a = np.array(im).astype(float)
    # puxa sombras/medios para o tom da marca (mais forte nas areas escuras)
    lum = a.mean(axis=2, keepdims=True) / 255.0
    w = (1.0 - lum) * tone
    a = a * (1 - w) + BRAND * w
    # leve aquecimento
    a[:, :, 0] *= warm
    a[:, :, 2] *= (2.0 - warm) * 0.5 + 0.47
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def emit(img, name, widths, quality=82):
    for w in widths:
        h = round(img.height * w / img.width)
        r = img.resize((w, h), Image.LANCZOS)
        r.save(f'assets/img/{name}-{w}.jpg', quality=quality, optimize=True, progressive=True)
        r.save(f'assets/img/{name}-{w}.webp', quality=quality - 4, method=6)
    print(name, widths, img.size)
