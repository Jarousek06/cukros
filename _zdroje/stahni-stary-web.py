#!/usr/bin/env python3
"""
Stáhne všechny fotky z původního webu cukros.cz v maximálním rozlišení.

Google Sites servíruje obrázky přes lh3.googleusercontent.com s parametrem
velikosti na konci adresy (např. =w1280). Když ho nahradíme za =w16383,
CDN pošle největší dostupnou variantu — u CUKROŠe typicky 2048 px.

Spuštění:  python cukros/_zdroje/stahni-stary-web.py
Výsledek:  _zdroje/fotky-web/ + prehled.html na proklikání
"""

import hashlib
import io
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Chybí Pillow: pip install Pillow")

HERE = Path(__file__).resolve().parent
OUT = HERE / "fotky-web"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"

STRANKY = {
    "/": "uvod",
    "/dorty": "dorty",
    "/chlebicky": "chlebicky",
    "/chutovky": "chutovky",
    "/kontakt": "kontakt",
    "/english": "english",
    "/chutovky_nejlepsi_vetrnik": "clanek-vetrnik",
    "/chutovky_caje": "clanek-caje",
    "/chutovky_26let_CUKROS": "clanek-onas",
    "/chutovky_Cafe_Reserva": "clanek-kava",
}

ADRESA = re.compile(r"https://lh3\.googleusercontent\.com/sitesv/[A-Za-z0-9_\-]+(?:=[A-Za-z0-9\-]+)?")


def stahni(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.cukros.cz/"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main():
    OUT.mkdir(exist_ok=True)

    # 1) posbírat adresy ze všech stránek
    kde = {}
    for cesta, jmeno in STRANKY.items():
        try:
            html = stahni("https://www.cukros.cz" + cesta).decode("utf-8", "ignore")
        except Exception as e:
            print(f"  {cesta:28} chyba: {e}")
            continue
        nalez = {u.split("=")[0] for u in ADRESA.findall(html)}
        for u in nalez:
            kde.setdefault(u, []).append(jmeno)
        print(f"  {cesta:28} {len(nalez):>3} obrázků")

    print(f"\nunikátních adres: {len(kde)}\n")

    # 2) stáhnout v maximu, zahodit duplicity a drobné ikonky
    otisky, ulozeno, malé, chyby = set(), [], 0, 0
    for i, (zaklad, stranky) in enumerate(sorted(kde.items()), 1):
        try:
            data = stahni(zaklad + "=w16383")
        except Exception:
            chyby += 1
            continue

        otisk = hashlib.sha1(data).hexdigest()
        if otisk in otisky:
            continue
        otisky.add(otisk)

        try:
            im = Image.open(io.BytesIO(data))
        except Exception:
            chyby += 1
            continue

        if min(im.size) < 400:          # ikonky a ozdoby ze šablony
            malé += 1
            continue

        im = im.convert("RGB")
        cista = Image.new("RGB", im.size)
        cista.paste(im)
        jmeno = f"{'-'.join(sorted(set(stranky)))[:40]}-{otisk[:6]}.jpg"
        cil = OUT / jmeno
        cista.save(cil, "JPEG", quality=90, optimize=True, progressive=True)
        ulozeno.append((cil, im.size, stranky))
        print(f"  [{i:>3}/{len(kde)}] {jmeno:52} {im.size[0]}×{im.size[1]}")

    # 3) přehled
    dlazdice = "".join(
        f'<figure><a href="{c.name}" target="_blank"><img src="{c.name}" loading="lazy"></a>'
        f'<figcaption>{c.name}<br>{r[0]}×{r[1]} · {", ".join(sorted(set(s)))}</figcaption></figure>'
        for c, r, s in sorted(ulozeno, key=lambda t: -t[1][0] * t[1][1])
    )
    (OUT / "prehled.html").write_text(f"""<!DOCTYPE html>
<html lang="cs"><head><meta charset="utf-8"><title>Fotky ze starého webu — {len(ulozeno)} ks</title>
<style>
 body{{margin:0;padding:2rem;background:#FBF7F3;font:14px/1.5 system-ui,sans-serif;color:#141010}}
 h1{{font-weight:400;font-size:1.6rem;margin:0 0 .3rem}} p{{color:#6E625E;max-width:62ch;margin:0 0 2rem}}
 .g{{display:grid;gap:1.2rem;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}}
 figure{{margin:0}} img{{width:100%;aspect-ratio:1;object-fit:cover;background:#F9DDEA;display:block;border-radius:2px}}
 figcaption{{font-size:11px;color:#6E625E;margin-top:.4rem;word-break:break-all}}
</style></head><body>
<h1>Fotky z původního webu cukros.cz</h1>
<p>{len(ulozeno)} fotek v maximálním rozlišení, seřazeno od největší.
V názvu je stránka, ze které fotka pochází.</p>
<div class="g">{dlazdice}</div></body></html>""", encoding="utf-8")

    print(f"\nuloženo: {len(ulozeno)}   přeskočeno malých: {malé}   chyb: {chyby}")
    print(f"složka:  {OUT}")
    print(f"přehled: {OUT / 'prehled.html'}")


if __name__ == "__main__":
    main()
