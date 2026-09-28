# CUKROŠ — web

Statický web pro cukrárnu a kavárnu CUKROŠ, Karlovo náměstí 72, Roudnice nad Labem.
Žádný build, žádné závislosti — jen HTML, CSS a jeden malý JS soubor.

## Struktura

```
cukros/
├── index.html        domovská stránka (zákusky, dorty, chlebíčky, zmrzlina, káva, snídaně, recenze, kontakt)
├── dorty.html        dorty na objednávku
├── chlebicky.html    chlebíčky a jednohubky
├── chutovky.html     rozcestník článků („Chuťovky“)
├── chutovky-vetrnik.html    článek: oceněný karamelový větrník
├── chutovky-caje.html       článek: čaje Dilmah a Madami
├── chutovky-26-let.html     článek: o cukrárně od roku 1998
├── chutovky-kava.html       článek: káva CAFÉ RESERVA
├── snidane.html      snídaně a brunch
├── faq.html          časté dotazy (+ strukturovaná data FAQPage)
├── kontakt.html      kontakt, otevírací doba, mapa
├── 404.html          chybová stránka (Netlify ji použije automaticky)
├── build.py          sestaví zminifikovanou verzi do dist/ a zabalí ZIP
├── dist/             výstup buildu — TOHLE se nasazuje (negenerovat ručně)
├── _zdroje/          podklady, na web nepatří
│   ├── stahni-fb-fotky.py   stáhne fotky z uložené FB stránky v plné kvalitě
│   ├── stahni-stary-web.py  stáhne fotky z cukros.cz v maximálním rozlišení
│   ├── fotky-web/           74 fotek ze starého webu + prehled.html
│   └── fotky-1440/          76 vašich fotek + prehled.html na výběr
└── assets/
    ├── css/style.css
    ├── js/main.js
    └── img/
        ├── logo-cukros.png   logo (na průhledném pozadí)
        ├── logo-lockup.png   logo s větším okolím (rezerva)
        └── mark-cake.png     samotná značka dortu (favicon, vodoznaky)
```

## Vizuální styl

Editorial styl velkých cukrářských domů (Pierre Hermé, Ladurée) přenesený
na vlastní identitu CUKROŠe:

| Token | Hodnota | Použití |
|---|---|---|
| `--rose` | `#F562A6` | firemní růžová vytažená přímo z loga |
| `--rose-deep` | `#C43B7C` | růžová pro text (dostatečný kontrast) |
| `--ink` | `#141010` | základní text, tmavé sekce |
| `--paper` | `#FBF7F3` | krémové pozadí |
| `--blush` / `--blush-2` | `#FDEEF5` / `#F9DDEA` | růžové sekce a foto-placeholdery |
| `--gold` | `#A9854C` | odznak ocenění (MF Dnes 2025) |

Písma: **Fraunces** (nadpisy) + **Jost** (text) z Google Fonts.
Fraunces je měkký patkový řez s vlastní povahou — nahradil Cormorant Garamond,
který je na prémiových webech okoukaný. Vrátit zpět = přepsat `--display`
v sekci 27.1 stylu na `"Cormorant Garamond"`.

### Prvky identity (sekce 27 ve stylu)

| Prvek | Co to je |
|---|---|
| **Pečeť 1998** | kroužící razítko „CUKROŠ · ROUDNICE NAD LABEM · ZALOŽENO 1998" se značkou dortu, přes roh fotky v sekci Poctivé řemeslo. Pod 900 px se skryje. |
| **Ornament `rule-mark`** | dělicí linka přerušená značkou dortu místo obyčejné čáry |
| **Odrážky** | značka dortu místo růžového kolečka v seznamech `.tick` |
| **Věta z tabule** | sekce `.statement` — sytě růžová přes celou šířku s vaší vlastní větou z tabule před podnikem |
| **Fotopás** | sekce `.showcase` — fotka přes celou šířku s nadpisem, který přes ni přetéká |

Růžová `--blush` byla ztmavena na `#FCE7F1`, aby na krémovém podkladu
skutečně četla jako růžová.

## Fotky

Fotky pocházejí z facebookového profilu CUKROŠe, staženy v plném rozlišení
(většina 1440×1440), na web zmenšeny na 1200 px a zkomprimovány.

### Carousely

Na webu jsou čtyři, všechny na stejném kódu (CSS `scroll-snap` + kousek JS,
žádná knihovna):

| Kde | Typ | Fotek | Interval |
|---|---|---|---|
| úvod → Poctivé řemeslo | jeden snímek přes celý sloupec | 4 | 7 s |
| úvod → Naše zákusky | pás, více fotek vedle sebe | 12 | 6 s |
| úvod → Dorty | jeden snímek | 3 | 6,5 s |
| Dorty → Druhy dortů | pás | 16 | 5,5 s |

Ovládají se šipkami, tečkami, šipkami na klávesnici, tažením prstem
i kolečkem myši. Posouvají se samy a **zastaví se natrvalo, jakmile do nich
uživatel sáhne**; při pouhém najetí myší se jen pauznou. Aktivní snímek se
pomalu přibližuje (Ken Burns, 7,5 s) a jeho popisek se vynoří.

Rychlost se řídí atributem `data-interval` (v milisekundách) přímo na
`<div class="carousel">`. Varianta přes celou šířku sloupce se zapne
třídou `carousel--single`.

Při zapnutém „omezit pohyb" v systému se neposouvají a nepřibližují vůbec.

Přidání fotky = vložit další `<figure class="slide">` do `[data-track]`;
tečky i počítadlo se dopočítají samy.

| Soubor | Popisek v carouselu | Rozlišení |
|---|---|---|
| `zakusky-vetrnik.jpg` | Karamelový větrník | 800×800 |
| `zakusky-malinovy-sen.jpg` | Malinový sen s bílou čokoládou | 800×800 |
| `zakusky-yuzu.jpg` | Yuzu — citrusová pěna | 800×800 |
| `zakusky-boruvkove-srdce.jpg` | Borůvkové srdce s bílou čokoládou | 800×800 |
| `zakusky-srdce.jpg` | Srdíčkové věnečky | 800×800 |
| `zakusky-venecky.jpg` | Věnečky s růžovou polevou | 800×800 |
| `zakusky-kupole.jpg` | Ovocné kupole s mochyní | 800×800 |
| `zakusky-rybiz.jpg` | Krémové řezy s rybízem | 800×800 |
| `zakusky-cokoladove.jpg` | Věnečky v čokoládě | 800×800 |
| `zakusky-spicky.jpg` | Čokoládové špičky | 800×800 |
| `zakusky-trubicky.jpg` | Krémové trubičky | 800×800 |
| `zakusky-pistaciovy.jpg` | Pistáciový řez | 800×800 |

**Popisky prosím zkontrolujte.** Tři z nich (Malinový sen, Yuzu, Borůvkové
srdce) jsou opsané přímo z popisků na fotkách, takže sedí jistě. Zbytek jsem
pojmenoval podle toho, co na fotce vidím — u větrníku a pistáciového řezu si
jsem dost jistý, u ostatních je to popis, ne oficiální název z vaší nabídky.
Opravit se dá v `index.html` v `<figcaption>` u příslušného slidu.

**Dorty na zakázku** v carouselu na stránce Dorty mají na sobě jména
zákazníků (Filip, Matyáš, Rozi, Jasmínka…). Jsou to fotky, které jste už
zveřejnili na svém Facebooku, takže je to v pořádku — ale kdyby vám to
u některé nesedělo, stačí říct a vyhodím ji.

### Ostatní fotky

| Soubor | Co je na ní | Rozlišení |
|---|---|---|
| `chlebicky.jpg` | krabice chlebíčků | 1200×1200 |
| `caj.jpg` | čajová nabídka se šálkem | 1200×1200 |
| `kava-cappuccino.jpg` | dvě kávy Café Reserva se šlehačkou | 1200×1200 |
| `dort-kvetinovy.jpg` | naked cake s jahodami a čokoládou | 1200×1200 |
| `dort-narozeninovy.jpg` | bílý dort s květy a trojkou | 1200×1200 |
| `dort-detsky.jpg` | dort s Pikachu | 1200×1200 |
| `dort-dzungle.jpg` | zelený dort s vílami | 1200×1200 |
| `interier-vitrina.jpg` | vitrína plná zákusků | 930×930 |
| `zakusky-tacek.jpg` | tácek se zákusky před cukrárnou | 526×701 |
| `zmrzlina-meloun.jpg` | melounový sorbet se zámkem | 526×701 |
| `zmrzlina-jahoda.jpg` | jahodový sorbet se zámkem | 526×701 |
| `zmrzlina-ruzova.jpg` | vana zmrzliny před podnikem | 526×701 |
| `vetrnik.jpg` | oficiální pečeť ocenění MF DNES + větrníky | 960×468 |
| `zmrzlina-tocena.jpg` | vanilková zmrzlina s bílou čokoládou | 1100×1100 |

**Točená zmrzlina v kornoutu chybí.** Fotka, kterou jste posílala, měla jen
206 px a mezi 117 staženými z Facebooku není. Sekce Zmrzlina proto ukazuje
vanilkovou zmrzlinu. Až fotku dodáte ve velkém (viz níže), stačí ji nahrát
jako `zmrzlina-tocena.jpg`.

### Jak z Facebooku dostat velkou fotku

Fotky uložené z **mřížky** na profilu mají jen 206 px — Facebook tam servíruje
náhledy. Postup pro plnou velikost:

1. Na fotku **klikněte**, ať se otevře v prohlížeči fotek
2. Teprve tam pravým tlačítkem → Uložit obrázek

Takhle dostanete 960 až 2048 px místo 206.
| `dort-svatebni.jpg` | čtyřpatrový svatební dort | 206×206 |

### Fotky ze starého webu

Skript `_zdroje/stahni-stary-web.py` stáhne fotky z cukros.cz. Google Sites
servíruje zmenšeniny přes parametr velikosti v adrese (`=w1280`); nahrazením
za `=w16383` pošle CDN největší variantu — u CUKROŠe typicky **2048 px**,
tedy víc než z Facebooku. Staženo 74 fotek do `_zdroje/fotky-web/`.

Odtud pochází svatební dort (1000×1000, nahradil poslední fotku v malém
rozlišení), čtyři chlebíčky do carouselu a větrník se zámkem.

**Snídaňové fotky ze starého webu jsem nepoužil.** Jsou to stock snímky —
generická stylizace, ateliérové světlo, nikde ani kus vaší cukrárny. Vaše
skutečné fotky mají v pozadí zámek, vitrínu nebo terasu. Sekce Snídaně
proto zatím ukazuje interiér kavárny; jakmile vyfotíte skutečný snídaňový
talíř, je to nejlepší místo, kam ho dát.

**Na webu už nezůstala žádná fotka v malém rozlišení.**

Na fotce větrníku je navíc **vlastní pečeť ocenění** (`.award-stamp`) —
kulaté razítko „Vítěz testu / MF DNES Sever · 2025“ se zlatým prstencem.
Nahradilo vypálenou přelepku z Facebooku.

### Jak stáhnout fotky z Facebooku ve velkém

Ve složce `_zdroje/` je skript **`stahni-fb-fotky.py`**:

```bash
python cukros/_zdroje/stahni-fb-fotky.py
```

Uložená facebooková stránka obsahuje jen náhledy 206×206, protože adresa
každého obrázku má parametr `ctp=s206x206`. Skript ho odstraní a CDN pošle
originál. Výsledek je v `_zdroje/fotky-1440/`:

- `cukros/` — 76 vašich fotek, k tomu `prehled.html` na proklikání
- `ostatni-necukros/` — 41 fotek z news feedu (cizí stránky, profilovky).
  **Ty na web nepatří, není to váš obsah.**

Adresy mají omezenou platnost (parametr `oe=`). Až přestanou fungovat,
uložte stránku na Facebooku znovu (Ctrl+S, „Webová stránka, kompletní")
do `_zdroje/` a skript pusťte na nový soubor.

**Lepší cesta pro budoucnost:** v Meta Business Suite nebo přes
„Stáhnout své informace" jde vyexportovat všechny fotky stránky najednou
v původní kvalitě, oficiálně a bez omezení platnosti. Úplně nejlepší jsou
pak originály přímo z telefonu, ty Facebook nikdy nekomprimoval.

## Co je potřeba doplnit

- [ ] Tři fotky v malém rozlišení (větrník, svatební dort, točená) — ideálně originály z telefonu
- [ ] Snídaňový talíř — v sekci Snídaně je zatím interiér kavárny
- [x] Facebook — <https://www.facebook.com/CukrosRCE>, odkaz je v patičce i v mobilním menu
- [ ] Instagram — profil se v podkladech nepodařilo dohledat, po dodání odkazu doplním
- [x] Texty článků — čtyři Chuťovky přeneseny z cukros.cz na vlastní stránky
- [ ] Ceník, pokud ho chcete zveřejňovat

## Ke zdrojovému kódu

Kód webu **nejde před návštěvníkem schovat** — prohlížeč musí HTML, CSS
i JS dostat, aby stránku vykreslil, takže je vždycky k přečtení
(Ctrl+U, F12, `curl`, uložení stránky). Blokování pravého tlačítka nebo
klávesových zkratek se obejde vypnutím JavaScriptu a hlavně otravuje
běžné návštěvníky, kteří si chtějí zkopírovat třeba telefonní číslo.

Co build dělá místo toho: minifikací se ze zdroje stane nečitelná zeď
textu bez komentářů. Není to ochrana, ale nikdo do toho nenakoukne ze
zvědavosti — a web se načte rychleji (HTML a CSS o ~20 %, JS o ~50 %).

Fotky si stejně kdokoliv uloží pravým tlačítkem; proti tomu technicky
nepomůže nic. Jediná reálná ochrana obsahu je autorské právo.

## Otevírací doba

Je na dvou místech — v HTML (`.hours`, patička) a v JS
(`assets/js/main.js`, pole `HOURS`), odkud se počítá živý stav
„Otevřeno / Zavřeno“ v hlavičce stránek. **Při změně upravte obě místa.**

## Lokální náhled

```bash
python -m http.server 5184 --directory cukros
```

Pak otevřít <http://localhost:5184>.

## Nasazení

Nasazuje se **zminifikovaná verze**, ne zdrojové soubory. Sestaví se takto:

```bash
python cukros/build.py
```

Skript také **přidá ke každému assetu otisk obsahu** (`vetrnik.jpg?v=4447ef38`).
Bez toho si prohlížeč po úpravě klidně nechá starou fotku — adresa se totiž
nezměnila. Otisk se mění s obsahem, takže změněný soubor se vždycky stáhne
znovu a nezměněný zůstane v cache. **Proto vždy nasazujte `dist/`, ne zdroj.**

Skript vyhodí z HTML, CSS i JS všechny komentáře a zalomení řádků,
uloží výsledek do `cukros/dist/` a rovnou z něj vytvoří
**`cukros-web.zip`** ve složce o úroveň výš. Potřebuje jen Node.js —
nástroje si `npx` stáhne sám.

Do balíčku nejde `README.md`, `build.py`, `_zdroje/` ani nepoužité
`logo-lockup.png`. Soubory jsou v kořeni ZIPu, takže `index.html`
sedí přesně tam, kde ho Netlify čeká.

**Upravovat se vždycky mají zdrojové soubory v `cukros/`, ne `dist/`** —
ten se při každém buildu maže a vytváří znovu.

- **Netlify Drop** — <https://app.netlify.com/drop>, přetáhnout `cukros-web.zip`
- **FTP** k současnému hostingu — rozbalit a nahrát obsah
- **GitHub Pages**

Po nasazení na vlastní doménu ještě upravit `<link rel="canonical">`
a `og:image` na absolutní URL.

## Údaje na webu

Vše převzato z původního webu cukros.cz a z firemního profilu:

- CUKROŠ, založeno 1998, IČO 61350796
- Karlovo náměstí 72, 413 01 Roudnice nad Labem
- Telefon / objednávky: +420 776 205 005
- E-mail: cukros@cukros.cz
- Po–So 7:30–18:00, Ne 8:30–18:00
- Snídaně: denně od otevření do 12:00 (malá, česká, francouzská, FIT) — potvrzeno
  na cukros.cz i na /english; pozor, původní web uvádí „od 7:30 každý den“,
  což v neděli neplatí, proto web říká jen „do 12:00“
- Hodnocení 4,5/5 z 321 recenzí na Google, cena na osobu 100–200 Kč
- Karamelový větrník — vítěz velkého testu karamelových větrníků,
  MF DNES Sever, 14. 2. 2025 (datum je čitelné na pečeti ve fotce `vetrnik.jpg`)
- Facebook: https://www.facebook.com/CukrosRCE


## Audit proti 20bodovému seznamu (8. 9. 2026)

Kompletně splněno: bez vodorovného posunu (ověřeno na 360 px), žádné rozbité
ani prázdné odkazy, mobilní menu na všech stránkách, favicon, unikátní titulky
i popisky, funkční patička, vlastní 404 s navigací, rok v patičce z JS,
komprimované fotky, klikatelné logo i všechna telefonní čísla a e-maily,
viewport všude.

**Formuláře na webu nejsou** — objednávky jdou telefonem, takže body
„success/error hlášky" nemají co ošetřovat. Až formulář přibude, hlášky
je potřeba doplnit.

**Náhledy pro sdílení**: `og:image` a `og:url` jsou absolutní a míří na
`cukros.netlify.app`. **Po přesunu na cukros.cz je nutné je přepsat** —
jinak se při sdílení na Facebooku načte obrázek ze staré adresy.


## Co přibylo po průzkumu konkurence (8. 9. 2026)

Prošel jsem 26 webů cukráren a pekáren (Ladurée, Levain, GAIL's, Poilâne,
Bo&Mie, Demel, Marchesi 1824, Black Star, Blikle, Erhart, Světozor a další)
a doplnil čtyři věci, které se u nich opakují nejvíc:

**Tři důvody** — sekce `#proc` hned pod běžícím pásem. Vlastní výroba od 1998,
vítěz testu MF DNES, suroviny z okolí. Vzorec, který má Světozor i Erhart.

**Dorty podle příležitosti** — `dorty.html` má místo jednoho míchaného
carouselu čtyři kategorie (svatební 3, narozeninové 4, dětské 6, na přání 4)
s rozcestníkem nahoře. **21 z 26 webů dělí sortiment do kategorií**, Cukroš
jako jediný ne. Kategorie mají `data-interval="0"`, takže se neposouvají samy —
čtyři běžící carousely na jedné stránce by rušily.

**Snídaně** (`snidane.html`) — vlastní stránka místo odstavce. Marchesi 1824
má snídaně jako plnohodnotnou kategorii sortimentu.

**Časté dotazy** (`faq.html`) — 8 otázek přes nativní `<details>`, žádný JS.
Obsahuje strukturovaná data `FAQPage`, takže se odpovědi můžou zobrazit rovnou
ve vyhledávání. Odpovědi vycházejí **jen z ověřených údajů**.

### Otázky, které potřebují potvrdit od CUKROŠe

Do FAQ jsem je nedal, protože je nemám z čeho ověřit:

- Pro kolik lidí je která velikost dortu (a ceny podle velikosti)
- Dá se platit kartou
- Vozíte dorty, nebo jen osobní odběr
- Kompletní seznam alergenů
- Dá se na dort dát fotka (jedlý tisk)

Až je budete mít, doplnění je otázka pěti minut — stačí přidat další
`<details>` blok do `faq.html` a otázku do skriptu strukturovaných dat.


## Ikony

Tři ikony v bloku „proč právě my" (kuchařská čepice, odznak ocenění, lahev
mléka) pocházejí ze sady **Lucide** — <https://lucide.dev>, licence **ISC**,
volně použitelné i komerčně. Jsou vložené přímo v HTML jako SVG, takže se
nic nestahuje zvenčí a zůstanou ostré na jakémkoliv displeji.

Tloušťka tahu je snížená z výchozích 2 na 1,7, aby ladily s jemností webu.
Barvu řídí `color` na `.pillar__ico` ve stylu.
