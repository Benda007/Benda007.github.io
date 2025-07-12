

# Evidence pojištěnců

Tento projekt je závěrečným testem kurzu pořádaného společností ITNetwork. Jedná se o konzolovou aplikaci pro správu evidence pojištěnců, která umožňuje přidávat, zobrazovat, vyhledávat a exportovat data pojištěnců.

## Soubory projektu

- **`main.py`**: Hlavní skript, který inicializuje aplikaci a spouští hlavní smyčku.
- **`insured.py`**: Obsahuje třídu `InsuredPerson`, která reprezentuje jednotlivé pojištěnce.
- **`insurance_agent.py`**: Obsahuje třídy `InsuranceAgent` a `RecordData`, které zajišťují logiku aplikace a manipulaci s daty o pojištěncích.

## Použití

Po spuštění programu budete mít na výběr z následujících možností:

1. **Přidat nového pojištěného**: Zadání nového pojištěnce. Program ověří správnost zadaných údajů jako jméno, příjmení, věk (1-80 let) a telefon.
2. **Vypsat všechny pojištěné**: Zobrazí seznam všech pojištěnců ve formátované podobě pro snadnější čitelnost.
3. **Vyhledat pojištěného**: Umožňuje vyhledat konkrétního pojištěnce podle jména a příjmení.
4. **Exportovat databázi**: Exportuje aktuální databázi pojištěnců do CSV souboru.
5. **Konec**: Ukončí program.

## Struktura kódu

- **`InsuredPerson`**: Třída, která definuje atributy pojištěnce jako jméno, příjmení, věk a telefon.
- **`InsuranceAgent`**: Obsahuje metody pro přidání záznamu, zobrazení pojištěnců, vyhledávání a export dat.
- **`RecordData`**: Obsahuje funkce pro zpracování uživatelského vstupu a jejich validaci, včetně normalizace telefonního čísla.

## Licence

Tento projekt je vytvořený jako testovací úloha a je určený pro výukové účely. 

## Kontakt

Projekt vytvořil Jean Kocman
