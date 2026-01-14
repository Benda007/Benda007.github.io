# API Dokumentace - CLI Funkce přes HTTP

Aplikace nyní podporuje spouštění CLI funkcí přes webové API. Tímto způsobem můžeš dělat všechno z webového frontend nebo cURL příkazů.

## Dostupné Endpoints

### 1. Filtrování Záznamů
**POST** `/api/filter`

Filtruje záznamy na základě kritérií.

**Příklad requestu:**
```bash
curl -X POST http://localhost:5000/api/filter \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John Doe",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "medication": "Aspirin",
    "diet": "Chocolate",
    "sleep": "Poor",
    "stress": "High",
    "effectiveness": "Yes",
    "intensity": 8
  }'
```

**Odpověď:**
```json
{
  "records": [[...], ...],
  "columns": ["id", "user_name", "date", ...],
  "count": 5
}
```

### 2. Editace Záznamu
**PUT** `/api/edit/<record_id>`

Edituje konkrétní záznam.

**Příklad requestu:**
```bash
curl -X PUT http://localhost:5000/api/edit/1 \
  -H "Content-Type: application/json" \
  -d '{
    "intensity": 7,
    "medication": "Ibuprofen",
    "effectiveness": "Yes"
  }'
```

**Odpověď:**
```json
{
  "message": "Record 1 updated successfully."
}
```

### 3. Smazání Záznamu
**DELETE** `/api/delete/<record_id>`

Smaže konkrétní záznam.

**Příklad requestu:**
```bash
curl -X DELETE http://localhost:5000/api/delete/1
```

**Odpověď:**
```json
{
  "message": "Record 1 deleted successfully."
}
```

### 4. Získání Uniqních Hodnot
**GET** `/api/unique-values?field=<field_name>`

Vrací seznam uniqních hodnot pro dané pole (pro výběr v frontend).

**Příklady requestů:**
```bash
# Uživatelé
curl http://localhost:5000/api/unique-values?field=users.user_name

# Data
curl http://localhost:5000/api/unique-values?field=headaches.date

# Léky
curl http://localhost:5000/api/unique-values?field=medications.medication

# Dieta
curl http://localhost:5000/api/unique-values?field=triggers.diet

# Spánek
curl http://localhost:5000/api/unique-values?field=triggers.sleep_quality

# Stres
curl http://localhost:5000/api/unique-values?field=triggers.stress_level

# Intenzita
curl http://localhost:5000/api/unique-values?field=headaches.intensity
```

**Odpověď:**
```json
{
  "field": "users.user_name",
  "values": ["John Doe", "Jane Smith", "Bob Johnson"]
}
```

### 5. Přidání Nového Záznamu
**POST** `/add`

Přidá nový záznam (původní endpoint).

**Příklad requestu:**
```bash
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "John Doe",
    "user_age": 30,
    "user_sex": "M",
    "date_of_headache": "2024-01-15",
    "time_of_headache": "14:30",
    "duration": 120,
    "intensity": 7,
    "trigger": "Chocolate",
    "headache_type": "Migraine",
    "medication": "Aspirin",
    "dosage": 500,
    "effectiveness": "Yes"
  }'
```

### 6. Získání Všech Záznamů
**GET** `/records`

Vrací všechny záznamy z databáze.

```bash
curl http://localhost:5000/records
```

### 7. Přehled Bolestí podle Triggerů
**GET** `/headaches_by_trigger`

Vrací počet bolestí podle každého triggeru.

```bash
curl http://localhost:5000/headaches_by_trigger
```

## Integrace s Frontend

Pro HTML frontend nyní můžeš:

1. **Filtrování** - zavolat `/api/filter` s JSON kriterií
2. **Editaci** - zavolat `/api/edit/<id>` s PUT requestem
3. **Smazání** - zavolat `/api/delete/<id>` s DELETE requestem
4. **Dynamické selecty** - zavolat `/api/unique-values?field=...` pro výběr možností

## Příklad Frontend Kódu

```javascript
// Filtrování záznamů
async function filterRecords() {
  const filter = {
    user_name: document.getElementById('userName').value,
    medication: document.getElementById('medication').value,
    intensity: parseInt(document.getElementById('intensity').value) || null
  };
  
  const response = await fetch('/api/filter', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(filter)
  });
  
  const data = await response.json();
  console.log('Filtered records:', data.records);
}

// Editace záznamu
async function editRecord(recordId) {
  const response = await fetch(`/api/edit/${recordId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      intensity: 6,
      effectiveness: 'Yes'
    })
  });
  
  const data = await response.json();
  console.log(data.message);
}

// Smazání záznamu
async function deleteRecord(recordId) {
  const response = await fetch(`/api/delete/${recordId}`, {
    method: 'DELETE'
  });
  
  const data = await response.json();
  console.log(data.message);
}

// Načtení unikátních hodnot pro filtr
async function loadFilterOptions() {
  const users = await fetch('/api/unique-values?field=users.user_name').then(r => r.json());
  const meds = await fetch('/api/unique-values?field=medications.medication').then(r => r.json());
  
  console.log('Available users:', users.values);
  console.log('Available medications:', meds.values);
}
```

## Shrnutí

Nyní máš možnost:
- ✅ Spouštět CLI operace přes HTTP API
- ✅ Používat je z webového frontend
- ✅ Kombinovat web a CLI funkcionalitu
- ✅ Nasadit na Render.com bez problémů
