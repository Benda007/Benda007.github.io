# Hra Člověče nezlob se

#### Video Demo: [Hra Člověče nezlob se-video](https://youtu.be/VCyraBtktCQ)

#### Popis:
**Hra Člověče nezlob se** je interaktivní webová verze oblíbené deskové hry, vyvinutá jako můj závěrečný projekt v rámci kurzu CS50x. Tato aplikace kombinuje moderní techniky webového vývoje pomocí HTML, CSS a JavaScriptu pro frontend a Python s Flaskem pro backend. Ukazuje soudržnou digitální rekreaci Ludo, s důrazem na robustní funkčnost a zapojení uživatelů.

## Přehled projektu

Hra replikovuje základní mechaniku Ludo, umožňuje více hráčům zapojit se do strategického hraní. Aplikace je navržena tak, aby simulovala dynamiku skutečné hry, jako je házení kostkou, pohyb figurek a automatizované řízení tahů, to vše v intuitivním a vizuálně příjemném rozhraní.

### Hlavní funkce

- **Responsivní uživatelské rozhraní**: Stylizováno pomocí Bootstrapu, aby bylo zajištěno, že rozložení je přizpůsobitelné napříč zařízeními a velikostmi obrazovek.
- **Interaktivní hraní**: Automatizovaná logika pro pohyb figurek a strategická herní rozhodnutí na základě výsledků hodu kostkou.
- **Dynamické UI komponenty**: Funkce jako animované figurky a indikátory stavu hráčů zvyšují interaktivní zážitek.

## Struktura souborů
### app.py

Tento Python soubor je středobodem projektu, běží server Flask pro zpracování webových požadavků. Flask funguje jako lehký, ale výkonný rámec pro integraci backendové funkčnosti s frontendovým rozhraním, což poskytuje optimální nastavení pro full-stack webový vývoj.

### templates/index.html

Definuje strukturální rozložení hry pomocí HTML. Jako šablona rozhraní nastavuje scénu pro design herního plánu, stav hráčů a integruje externí styly a skripty pro funkčnost.

### static/styles.css

Obsahuje pravidla stylizace, která definují estetiku hry. Využívá CSS spolu s Bootstrapem, aby vytvořila responsivní a vizuálně odlišné herní prostředí s jasným rozlišením pro figurky hráčů a stav herního plánu.

### static/script.js

Obsahuje JavaScriptovou logiku, která je centrální pro herní mechaniku a interaktivitu. Funkce řídí tok hry, jako jsou pohyby figurek, přechody mezi tahy hráčů a animace, což zajišťuje plynulé hraní.

## Designové volby

Několik promyšlených designových rozhodnutí tvoří základ tohoto projektu:

- **Integrace backendu s Flaskem**: Zvolen pro svou jednoduchost a škálovatelnost, Flask usnadňuje snadné rozšíření aplikace, například budoucí připojení databáze pro ukládání stavu hry.
- **Full-Stack vývoj**: Použití Pythonu a Flaska poskytuje schopnosti, které přesahují to, co mohou dosáhnout pouze HTML, CSS a JavaScript. To umožňuje serverové výpočty, snadnější správu stavů aplikace a hladkou integraci databází (např. SQL pro ukládání pokroku ve hře), čímž se vytváří základ pro pokročilé funkce.
- **Automatizace herní logiky**: Implementace automatických tahů pro figurky, když dosáhnou strategických herních pozic, odráží zaměření na zlepšení uživatelského zážitku a použitelnosti.

## Budoucí vývoj

Významnou oblastí pro budoucí práci je implementace trvalého ukládání stavu hry pomocí SQL databáze. To umožní funkce jako:
- **Trvalost stavu hry**: Umožnit hráčům pokračovat ve hrách později.
- **Statistiky hráčů**: Sledovat a zobrazovat historická data o odehraných hrách, což zvyšuje zapojení prostřednictvím žebříčků a analýzy výkonu.
- **Optimalizace hraní**: Vzhledem
