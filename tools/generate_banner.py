"""Generate the GitHub profile banners from avatar.png.

The source image and this script are the source of truth; generated SVGs are
deliberately checked in so GitHub can serve them directly.
"""
from pathlib import Path
import html
import random
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

W, H = 1180, 610
PX, PY, PW, PH = 54, 144, 372, 392


def dither(image: Image.Image, isolate_subject: bool) -> np.ndarray:
    """Floyd–Steinberg dither in serpentine order at the final dot grid."""
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.3)
    gray = gray.filter(ImageFilter.UnsharpMask(radius=3, percent=140))
    a = np.asarray(gray.resize((186, 196), Image.Resampling.LANCZOS), dtype=float)
    # The avatar is dark subject on light background. Keep the dark ink.
    a = 255 - a
    for y in range(a.shape[0]):
        xs = range(a.shape[1]) if y % 2 == 0 else range(a.shape[1] - 1, -1, -1)
        for x in xs:
            old = a[y, x]
            new = 255 if old >= 118 else 0
            err = old - new
            a[y, x] = new
            direction = 1 if y % 2 == 0 else -1
            for dx, dy, weight in ((direction, 0, 7), (-direction, 1, 3), (0, 1, 5), (direction, 1, 1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < a.shape[1] and ny < a.shape[0]:
                    a[ny, nx] += err * weight / 16
    bits = a > 0
    if isolate_subject:
        # The supplied photo has a busy outdoor background. This tapered mask
        # preserves head/shoulders in dark mode without turning foliage into ink.
        yy, xx = np.ogrid[:bits.shape[0], :bits.shape[1]]
        head = ((xx - 93) / 51) ** 2 + ((yy - 59) / 66) ** 2 < 1
        shoulders = ((xx - 93) / 83) ** 2 + ((yy - 142) / 69) ** 2 < 1
        bits &= head | shoulders
    return bits


def dot_paths(bits: np.ndarray, hue: str) -> str:
    paths = []
    for y, row in enumerate(bits):
        x = 0
        while x < len(row):
            if not row[x]:
                x += 1
                continue
            start = x
            while x < len(row) and row[x]:
                x += 1
            # tight horizontal runs render crisply and keep file size modest
            x1 = PX + start * 2
            x2 = PX + x * 2 - 0.55
            yy = PY + y * 2
            paths.append(f'<path d="M{x1:.1f} {yy:.1f}h{x2-x1:.1f}"/>')
    return f'<g class="portrait-dots" stroke="{hue}">' + ''.join(paths) + '</g>'


def rows(values, color):
    out = []
    y = 182
    for label, value in values:
        label = html.escape(label.upper())
        value = html.escape(value)
        dots = '.' * max(3, 38 - len(label) - len(value))
        out.append(f'<text x="490" y="{y}" class="label">{label}</text><text x="598" y="{y}" class="leader">{dots}</text><text x="1088" y="{y}" class="value" text-anchor="end">{value}</text>')
        y += 23
    return ''.join(out)


def build(mode: str):
    dark = mode == 'dark'
    bg, panel, line, ink, muted, portrait = (
        ('#0A101F', '#0E172A', '#1E3850', '#D7F8FF', '#75A7B7', '#A78BFA') if dark else
        ('#F7FBFF', '#FFFFFF', '#C6E4EE', '#0A3040', '#547983', '#7C3AED')
    )
    image = Image.open(ROOT / 'photoGraph.jpeg').convert('RGB')
    # Head-and-shoulders framing: avoids the aggressive tight-face crop.
    image = image.crop((22, 230, 458, 690))
    bits = dither(image, isolate_subject=dark)
    values = [
        ('Subject', 'Javed Akhtar'), ('Role', 'Full Stack Developer'),
        ('Origin', 'Gurugram, Haryana, India'), ('Education', 'Software Engineering'),
        ('Status', 'Building AI-powered enterprise systems'),
        ('ToolChain', 'Python · FastAPI · Angular · Docker'),
        ('Core.Lang', 'Python · TypeScript · JavaScript'), ('Core.Frontend', 'Angular · React · Next.js'),
        ('Core.Backend', 'FastAPI · Node.js · REST'), ('Core.Database', 'MySQL · MongoDB · Redis'),
        ('Core.Infra', 'Docker · IIS · Linux'), ('Grid.Mail', 'javedsir301@gmail.com'),
        ('Grid.Portfolio', 'javed-akhtar-portfolio.vercel.app'), ('Grid.LinkedIn', 'in/javedsir301'),
        ('Grid.GitHub', 'github.com/javedsir301')]
    random.seed(301)
    spark = ''.join(f'<circle cx="{PX+random.random()*PW:.1f}" cy="{PY+random.random()*PH:.1f}" r="1" class="spark" style="animation-delay:-{random.random()*2:.2f}s"/>' for _ in range(64))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="610" viewBox="0 0 1180 610" role="img" aria-label="Javed Akhtar developer profile banner">
<style>
@keyframes enter {{ from {{ opacity:0 }} to {{ opacity:1 }} }}
@keyframes pulse {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.28 }} }}
.title{{font:600 15px ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:1.8px;fill:{muted}}}.label{{font:600 12px ui-monospace,SFMono-Regular,Consolas,monospace;letter-spacing:1px;fill:{muted}}}.leader{{font:12px ui-monospace,SFMono-Regular,Consolas,monospace;fill:{line}}}.value{{font:500 13px ui-monospace,SFMono-Regular,Consolas,monospace;fill:{ink}}}.portrait-dots{{stroke-width:1.35;stroke-linecap:square;shape-rendering:crispEdges;animation:enter 2s ease-out both}}.spark{{fill:#22D3EE;animation:pulse 2s ease-in-out infinite}}.live{{animation:pulse 1.2s ease-in-out infinite}}</style>
<rect width="1180" height="610" rx="14" fill="{bg}"/><rect x="20" y="20" width="1140" height="570" rx="10" fill="{panel}" stroke="{line}"/>
<path d="M20 82H1160M456 82V590" stroke="{line}"/>
<circle cx="48" cy="51" r="6" fill="#FB7185"/><circle cx="70" cy="51" r="6" fill="#FBBF24"/><circle cx="92" cy="51" r="6" fill="#10B981"/>
<text x="122" y="56" class="title">profile.sh --live</text><text x="1098" y="56" class="title" text-anchor="end">JAVED AKHTAR / 2026</text>
<rect x="45" y="118" width="392" height="438" rx="7" fill="{bg}" stroke="{line}"/><text x="62" y="143" class="title">VISUAL.MAP / AVATAR</text>
<clipPath id="portrait"><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="3"/></clipPath><g clip-path="url(#portrait)">{dot_paths(bits, portrait)}{spark}</g>
<path d="M54 536H426" stroke="{line}"/><text x="62" y="548" class="label">DITHERED IDENTITY SIGNAL</text>
<text x="490" y="128" class="title">SYSTEM.INFO</text><circle cx="960" cy="123" r="5" fill="#FB7185" class="live"/><text x="974" y="128" class="label" fill="#FB7185">LIVE</text><rect x="1030" y="105" width="72" height="28" rx="14" fill="#0891B2"/><text x="1066" y="124" text-anchor="middle" class="label" fill="#fff">@javedsir301</text>
{rows(values, ink)}<text x="490" y="555" class="label">01 / SYSTEM ONLINE</text><path d="M707 551h381" stroke="#10B981" stroke-width="3"/>
</svg>'''
    (OUT / f'{mode}.svg').write_text(svg, encoding='utf-8')


if __name__ == '__main__':
    build('dark')
    build('light')
