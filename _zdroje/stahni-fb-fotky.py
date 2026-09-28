#!/usr/bin/env python3
"""
Stáhne fotky z uložené facebookové stránky v plném rozlišení.

Jak to funguje
--------------
Když si uložíte facebookovou stránku (Ctrl+S → „Webová stránka, kompletní"),
uloží se jen NÁHLEDY fotek, typicky 206×206 px. Ale v adrese každého náhledu
je parametr `ctp=s206x206`, který CDN říká „pošli mi zmenšeninu".
Když ho odstraníme, stejná adresa vrátí originál — u CUKROŠe 1440×1440 px.

Použití
-------
    python stahni-fb-fotky.py

Fotky se uloží do složky `fotky-1440/` vedle skriptu, k tomu `prehled.html`,
kde si je můžete proklikat a vybrat.

Důležité
--------
Adresy obsahují podpis s platností (parametr `oe=`) — po několika hodinách
až dnech přestanou fungovat. Pak je potřeba stránku na Facebooku znovu
uložit a skript spustit na čerstvý soubor.

Stahují se jen fotky z vaší vlastní stránky, jejichž adresy už v souboru
jsou. Skript se nikam nepřihlašuje a nic neobchází.
"""

import hashlib
import html as html_mod
import io
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Chybí Pillow. Nainstalujte: pip install Pillow")

HERE = Path(__file__).resolve().parent
OUT = HERE / "fotky-1440"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"


def najdi_ulozenou_stranku():
    kandidati = sorted(HERE.glob("*.html"), key=lambda p: p.stat().st_size, reverse=True)
    if not kandidati:
        sys.exit(f"Ve složce {HERE} není žádný .html soubor s uloženou stránkou.")
    return kandidati[0]


def najdi_adresy(soubor):
    raw = soubor.read_text(encoding="utf-8", errors="ignore")
    raw = raw.replace("\\/", "/")
    nalezene = re.findall(r'https://scontent[^"\'\s<>\\]+?ctp=s\d+x\d+[^"\'\s<>\\]*', raw)
    adresy = []
    videno = set()
    for u in nalezene:
        u = html_mod.unescape(u)
        plna = re.sub(r"&ctp=s\d+x\d+", "", u)
        # id fotky = první číslo v názvu souboru na CDN
        m = re.search(r"/([0-9]+_[0-9]+_[0-9]+)_n\.", plna)
        klic = m.group(1) if m else plna
        if klic in videno:
            continue
        videno.add(klic)
        adresy.append((klic, plna))
    return adresy


def stahni(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.facebook.com/"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def main():
    soubor = najdi_ulozenou_stranku()
    adresy = najdi_adresy(soubor)
    print(f"Zdroj: {soubor.name}")
    print(f"Nalezeno fotek: {len(adresy)}\n")
    if not adresy:
        sys.exit("Žádné adresy fotek. Uložil se opravdu kompletní web (ne jen HTML)?")

    OUT.mkdir(exist_ok=True)
    hotovo, chyby, duplicity = [], [], 0
    otisky = set()

    for i, (klic, url) in enumerate(adresy, 1):
        cil = OUT / f"{klic}.jpg"
        if cil.exists():
            print(f"[{i:>3}/{len(adresy)}] {klic[:24]:26} už staženo")
            hotovo.append(cil)
            continue
        try:
            data = stahni(url)
        except urllib.error.HTTPError as e:
            print(f"[{i:>3}/{len(adresy)}] {klic[:24]:26} CHYBA {e.code}"
                  f"{'  (adresa vypršela — ulož stránku znovu)' if e.code in (403, 410) else ''}")
            chyby.append(klic)
            continue
        except Exception as e:
            print(f"[{i:>3}/{len(adresy)}] {klic[:24]:26} CHYBA {e}")
            chyby.append(klic)
            continue

        otisk = hashlib.sha1(data).hexdigest()
        if otisk in otisky:
            duplicity += 1
            print(f"[{i:>3}/{len(adresy)}] {klic[:24]:26} duplicita, přeskočeno")
            continue
        otisky.add(otisk)

        im = Image.open(io.BytesIO(data)).convert("RGB")
        cista = Image.new("RGB", im.size)     # zahodí metadata
        cista.paste(im)
        cista.save(cil, "JPEG", quality=90, optimize=True, progressive=True)
        print(f"[{i:>3}/{len(adresy)}] {klic[:24]:26} {im.size[0]}×{im.size[1]}  {cil.stat().st_size//1024} kB")
        hotovo.append(cil)

    # přehledová stránka
    dlazdice = "\n".join(
        f'<figure><a href="{f.name}" target="_blank"><img src="{f.name}" loading="lazy"></a>'
        f'<figcaption>{f.name}</figcaption></figure>'
        for f in sorted(hotovo)
    )
    (OUT / "prehled.html").write_text(f"""<!DOCTYPE html>
<html lang="cs"><head><meta charset="utf-8">
<title>Fotky z Facebooku — {len(hotovo)} ks</title>
<style>
 body{{margin:0;padding:2rem;background:#FBF7F3;font:14px/1.5 system-ui,sans-serif;color:#141010}}
 h1{{font-weight:400;margin:0 0 .3rem}} p{{color:#6E625E;margin:0 0 2rem}}
 .g{{display:grid;gap:1.2rem;grid-template-columns:repeat(auto-fill,minmax(220px,1fr))}}
 figure{{margin:0}} img{{width:100%;aspect-ratio:1;object-fit:cover;background:#F9DDEA;display:block}}
 figcaption{{font-size:11px;color:#6E625E;word-break:break-all;margin-top:.4rem}}
</style></head><body>
<h1>Fotky z Facebooku CUKROŠ</h1>
<p>{len(hotovo)} fotek v plném rozlišení. Klikněte pro zvětšení.</p>
<div class="g">{dlazdice}</div>
</body></html>""", encoding="utf-8")

    print(f"\nStaženo: {len(hotovo)}   duplicit: {duplicity}   chyb: {len(chyby)}")
    print(f"Složka:  {OUT}")
    print(f"Přehled: {OUT / 'prehled.html'}")


if __name__ == "__main__":
    main()
