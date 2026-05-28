import re
import sys
from pathlib import Path
# ensure project root is on sys.path for relative path resolution
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

def hex_to_rgb(hexc):
    h = hexc.lstrip('#')
    if len(h)==3:
        h=''.join([c*2 for c in h])
    return tuple(int(h[i:i+2],16)/255.0 for i in (0,2,4))

def luminance(rgb):
    def channel(c):
        if c<=0.03928:
            return c/12.92
        return ((c+0.055)/1.055)**2.4
    r,g,b = rgb
    return 0.2126*channel(r)+0.7152*channel(g)+0.0722*channel(b)

def contrast_ratio(hex1, hex2):
    a = luminance(hex_to_rgb(hex1))
    b = luminance(hex_to_rgb(hex2))
    L1 = max(a,b)
    L2 = min(a,b)
    return (L1+0.05)/(L2+0.05)

# Read base.html and extract CSS variables and colors
base_path = Path(__file__).resolve().parents[1] / 'web' / 'templates' / 'web' / 'base.html'
base = base_path.read_text(encoding='utf-8')
style_block = re.search(r"<style>(.*?)</style>", base, re.S)
css = style_block.group(1) if style_block else base

vars = dict(re.findall(r"--([a-z0-9\-]+):\s*([^;\n]+);", css))
# find body color
body_color = None
m = re.search(r"body\s*\{[^}]*color:\s*([^;\n]+);", css)
if m:
    body_color = m.group(1).strip()
# normalize colors (only hex supported)
for k,v in vars.items():
    vars[k] = v.strip()

bg = vars.get('bg-dark') or '#000000'
accent = vars.get('accent') or '#ffffff'
muted = vars.get('muted') or '#888888'
body = body_color or '#ffffff'

# ensure hex format
def normalize(hexval):
    if hexval.startswith('#'):
        return hexval
    # try to find hex in the string
    hx = re.search(r"#([0-9a-fA-F]{3,6})", hexval)
    if hx:
        return '#'+hx.group(1)
    return '#000000'

bg = normalize(bg)
accent = normalize(accent)
muted = normalize(muted)
body = normalize(body)

print('Colors found:')
print(' bg', bg)
print(' body', body)
print(' accent', accent)
print(' muted', muted)

print('\nContrast ratios (against background):')
print(' body vs bg:', round(contrast_ratio(body,bg),2))
print(' accent vs bg:', round(contrast_ratio(accent,bg),2))
print(' muted vs bg:', round(contrast_ratio(muted,bg),2))

# Recommendations
b = contrast_ratio(body,bg)
a = contrast_ratio(accent,bg)
m = contrast_ratio(muted,bg)

print('\nRecommendations:')
if b < 4.5:
    print('- Body text contrast is below 4.5:1 — consider lightening body color or darkening background.')
else:
    print('- Body text contrast OK for normal text (>=4.5).')

if a < 3 and a< b:
    print('- Accent color contrast is low for small text; consider using accent only for large titles or increasing contrast.')
else:
    print('- Accent contrast seems acceptable for decorative/large text.')

if m < 4.5:
    print('- Muted text has low contrast for normal text; use it only for secondary elements or increase contrast.')
else:
    print('- Muted contrast OK.')
