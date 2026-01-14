# Nasazení na Render.com

## Příprava projektu

Projekt je nyní připraven na nasazení na **Render.com**. Foram byly provedeny následující změny:

### Provedené úpravy:

1. **api.py** - Aplikace nyní poslouchá na adrese `0.0.0.0` a portu ze proměnné `PORT`
   - `debug` je nastaven na `False` pro produkci
   
2. **.gitignore** - Přidán soubor ignorující nepotřebné adresáře a soubory
   
3. **runtime.txt** - Specifikuje Python verzi 3.11.7
   
4. **.env.example** - Příklad proměnných prostředí

5. **Procfile** - Již správně nakonfigurován pro gunicorn

## Kroky k nasazení na Render.com:

### 1. Push do GitHub
```bash
cd /workspaces/Benda007.github.io/projects/project2
git add .
git commit -m "Příprava na Render.com nasazení"
git push origin main
```

### 2. Vytvoření nové služby na Render.com

1. Přejděte na [render.com](https://render.com)
2. Klikněte na **"New"** → **"Web Service"**
3. Připojte svůj GitHub účet (pokud již není připojen)
4. Vyberte repository: **Benda007.github.io**
5. Vyberte adresář: **projects/project2**

### 3. Konfigurace nasazení

- **Name:** `headache-tracker` (nebo jiný název)
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn myapp.api:app`
- **Instance Type:** Free (nebo vyšší podle potřeby)

### 4. Environment Variables (pokud potřeba)

V nastavení Render.com přejděte do **Environment** a přidejte:
```
PORT=5000
FLASK_ENV=production
```

## Instalace dependencí (lokálně pro test)

```bash
pip install -r requirements.txt
```

## Spuštění aplikace lokálně

```bash
python -m myapp.api
```

Aplikace bude dostupná na `http://localhost:5000`

## Poznámky

- Aplikace používá SQLite databázi (`myapp/headache.db`)
- Pro produkci zvažte použití PostgreSQL místo SQLite
- Ujistěte se, že máte v `.gitignore` soubor `headache.db`, pokud jej chcete ignorovat

## Troubleshooting

Pokud narazíte na problémy:
1. Zkontrolujte logy v Render.com dashboardu
2. Ujistěte se, že všechny dependence jsou v `requirements.txt`
3. Ověřte, že aplikace poslouchá na správném portu
