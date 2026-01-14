# Headache Tracker - Hybrid CLI/Web Mode

## Přehled

Aplikace nyní běží v **hybridním módu**, kde si uživatel může vybrat mezi:
- **CLI (Command Line Interface)** - textové menu v terminálu
- **Web Interface (HTML)** - webové rozhraní v prohlížeči

## Jak spustit aplikaci

### Standardní spuštění (Interactive Menu)

```bash
python project.py
```

Zobrazí se vám interaktivní menu:

```
============================================================
📋 HEADACHE TRACKER - Main Menu
============================================================
1. View all records
2. Add a new headache record
3. Filter records by criteria
4. Edit or delete a record
5. Export records to Excel
6. Import records from Excel
7. Switch to Web Interface (HTML)
8. Exit
============================================================
```

### Spuštění příkazů z terminálu (CLI mode)

Stále můžete používat příkazové argumenty jako dříve:

```bash
# Přidání nového záznamu
python project.py --add

# Filtrování záznamů
python project.py --filter

# Editace/smazání záznamů
python project.py --edit
python project.py --delete

# Export do Excel
python project.py --export --file data.xlsx

# Import z Excel
python project.py --upload --file data.xlsx

# Zobrazení všech záznamů
python project.py

# Přímé spuštění web rozhraní
python project.py --web
```

## Přepínání mezi CLI a Web Interface

### CLI → Web Interface

1. V interaktivním menu vyberte volbu **7** (Switch to Web Interface)
2. Otevře se webové rozhraní v prohlížeči (http://localhost:5000)
3. Můžete si vybrat mezi:
   - Přidáním nových záznamů
   - Prohlížením tabulky
   - Prohlížením grafu
   - Filtrováním záznamů

### Web Interface → CLI

1. Na webové stránce klikněte na tlačítko **⬅️ Return to CLI** v horní části
2. Otevře se okno s instrukcemi
3. Stiskněte **Ctrl+C** v terminálu
4. CLI menu se automaticky vrátí

## Struktura aplikace

```
project2/
├── project.py                 # Main entry point s CLI menu
├── myapp/
│   ├── api.py                 # Flask webový server
│   ├── db.py                  # Databázová logika
│   ├── core.py                # Filtrování a logika
│   ├── headache.db            # SQLite databáze
│   ├── templates/
│   │   └── index.html         # Web frontend
│   └── static/
│       ├── js/
│       │   └── script.js       # JavaScript pro web
│       └── css/
│           └── styles.css     # Styling
├── requirements.txt
└── Procfile                   # Pro Render.com
```

## Render.com Nasazení

Na Render.com se aplikace standardně spouští v CLI interactive menu:

```
Build Command: pip install -r requirements.txt
Start Command: python project.py
```

Projekt běží v defaultním CLI módu, kde si uživatel může:
1. Vybrat jednu z 8 opcí CLI menu
2. Nebo si otevřít web rozhraní pokud chce grafické UI

## API Endpoints (pro web interface)

Webové rozhraní komunikuje s těmito API endpoints:

- **GET** `/` - Hlavní stránka (HTML)
- **POST** `/add` - Přidání nového záznamu
- **GET** `/records` - Zobrazení všech záznamů
- **GET** `/headaches_by_trigger` - Statistiky podle triggerů
- **POST** `/api/filter` - Filtrování záznamů
- **PUT** `/api/edit/<id>` - Editace záznamu
- **DELETE** `/api/delete/<id>` - Smazání záznamu
- **GET** `/api/unique-values` - Dostupné hodnoty pro filtry
- **GET** `/api/stop` - Informace o návratu do CLI

## Klíčové výhody

✅ **Minimální změny** - Existující kód zůstává nechangen
✅ **Flexibilita** - Uživatel si vybere, co mu vyhovuje (CLI nebo Web)
✅ **Seamless přepínání** - Snadno se přepínat mezi oběma módy
✅ **Render.com kompatibilní** - Pracuje bez problémů
✅ **Všechny funkce** - Všechny operace dostupné v obou módech

## Příklady použití

### Scénář 1: Jen CLI
```bash
python project.py
# Vybere menu → Vybere operaci → Vrátí se do menu
# Opakuje se dokud uživatel nevybere "Exit" (8)
```

### Scénář 2: Jen Web
```bash
python project.py --web
# Otevře se http://localhost:5000
# Uživatel pracuje v prohlížeči
# Ctrl+C zastaví server
```

### Scénář 3: Hybridní (CLI + Web)
```bash
python project.py
# Menu → Vybere "Switch to Web Interface" (7)
# Web interface otevřen
# Klikne "Return to CLI"
# Ctrl+C → Vrátí se do menu
```

## Troubleshooting

**Q: Tlačítko "Return to CLI" nefunguje**
A: Je to design feature - jednoduše stiskněte Ctrl+C v terminálu

**Q: Server se neukončuje**
A: Stiskněte Ctrl+C v terminálu, kde běží server

**Q: Port 5000 je už obsazený**
A: Změňte PORT: `PORT=8000 python project.py --web`

## Závěr

Aplikace nyní nabízí nejlepší z obou světů:
- **CLI** pro quick operace a scripting
- **Web** pro intuitivní a vizuální interakci

Přepínání mezi nimi je hladké a uživatelsky přívětivé! 🎉
