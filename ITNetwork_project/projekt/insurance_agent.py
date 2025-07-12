import re
import csv
from insured import InsuredPerson


class InsuranceAgent:
    # definujeme šírky sloupců pro tabulku, která bude vytištěna v terminálů. Účelem je vyhnout se magic numbers.
    CW = COLUMN_WIDTHS = {
        'index': 5,
        'name': 15,
        'surname': 15,
        'age': 6,
        'phone': 15
    }

    def __init__(self, insured): # původně bez insured, pouze prázný seznam-list
        self.insured_list = insured #[] původně jen prázný list, nově pojmenovaný, aby se s ním dalo pracovat
    # definice pro přidání záznamu
    def add_record(self, insured):
        self.insured_list.append(insured)
    # definice pro ukázku všech záznamů v databázi již zadaných
    def show_insured(self):
        if not self.insured_list:
            print("Databáze je prázdná. Prosím, nejdříve zadejte nějakého pojištěnce.")
        else:
            header = f"{'č.':<{self.CW['index']}} {'Jméno':<{self.CW['name']}} {'Příjmení':<{self.CW['surname']}} {'Věk':<{self.CW['age']}} {'Telefon':<{self.CW['phone']}}"
            print(header)
            print("-" * len(header))
            for index, insured in enumerate(self.insured_list, start=1):
                print(
                    f"{index:<{self.CW['index']}} {insured.name:<{self.CW['name']}} {insured.surname:<{self.CW['surname']}} {insured.age:<{self.CW['age']}} {insured.phone:<{self.CW['phone']}}")

    # definice vyhledání v databázi
    def search_insured(self, name, surname):
        if not self.insured_list:
            print("Databáze je prázdná. Prosím, nejdříve zadejte nějakého pojištěnce.")
            return None
        else:
            for insured in self.insured_list:
                if insured.name == name and insured.surname == surname:
                    return insured
        return None
    # definice exportu obsahu databáze do CSV
    def export_database(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # vyexportuje data ve sloupcích s údaji indes, jméno atd...
            writer.writerow(['Index', 'Name', 'Surname', 'Age', 'Phone'])
            for index, insured in enumerate(self.insured_list, start=1):
                writer.writerow([index, insured.name, insured.surname, insured.age, insured.phone])
        print(f"Export databáze do souboru {filename} proběhl úspěšně.")

# záznam údajů do databáze
class RecordData:
    def __init__(self):
        self.agent = InsuranceAgent(insured=[]) #
    # převede telefonní číslo na upravený lépe čitelný formát
    def normalize_phone_number(self, phone):
        # ze začátku čísla odstraníme všechny nečíselné znaky, kromě + kvůli mezinárodní volbě
        normalized_phone = re.sub(r'(?!^\+)\D', '', phone)
        if phone.startswith('+'):
            normalized_phone = normalized_phone[1:]  # Remove the leading '+'
            # chceme čísla seskupit po 3 od zadu, proto ho musíme otočit
            reversed_phone = normalized_phone[::-1]
            formatted_phone = re.sub(r'(\d{3})(?=\d)', r'\1 ', reversed_phone)
            formatted_phone = formatted_phone[::-1]
            # číslo je seskupené, opět ho otočíme do výchozího stavu
            return f"+{formatted_phone}"
        else:
            # stejně jako předešlá část, jen platí pro čísla bez + na začátku
            if not normalized_phone.isdigit():
                return None
            reversed_phone = normalized_phone[::-1]
            formatted_phone = re.sub(r'(\d{3})(?=\d)', r'\1 ', reversed_phone)
            return formatted_phone[::-1]

    # Zde ošetříme situaci, kdy jméno může obsahovat pomlčku.
    def validate_name(self, name):
        return all(part.isalpha() for part in name.split('-')) and name

    # ověření příjmení - pro zachování DRY
    def validate_surname(self, surname):
        return surname.isalpha() and surname

    # zajistíme, že věk pojištěnce bude min 1 a max 99 resp. jedno až dvouciferné číslo
    def validate_age(self, age):
        return age.isdigit() and 1 <= int(age) <= 80


    def validate_phone(self, phone):
        return bool(phone.strip().isdigit()) and len(phone) >=9

    # ošetření operací které uživatel může zadat
    # Zadáme jméno. Může obsahovat pouze písmena a pomlčku. První písmeno bude převedeno na velké.
    def get_user_input(self):
        while True:
            # během zadávání může uživatel celou operaci zrušit zapsáním 'cancel'
            name = input("Zadejte jméno (nebo napište 'cancel' pro zrušení): ").strip()
            if name.lower() == 'cancel':
                print("Vkládání nového pojištěnce bylo zrušeno.")
                break
            if not self.validate_name(name):
                print("Jméno smí obsahovat pouze písmena či pomlčky a nesmí být prázdné. Opakujte zadání.")
                continue
            name = '-'.join(part.capitalize() for part in name.split('-'))
            break
        # Zadáme příjmení.  Může obsahovat pouze písmena. První písmeno bude převedeno na velké.
        while True:
            surname = input(
                "Zadejte příjmení (nebo napište 'cancel' pro zrušení): ").strip().capitalize()
            if surname.lower() == 'cancel':
                print("Vkládání nového pojištěnce bylo zrušeno.")
                break
            if not self.validate_surname(surname):
                print("Příjmení smí obsahovat pouze písmena. Opakujte zadání.")
                continue
            break
        # Zadáme věk v rozmezí 1 - 80 let včetně. Jiné věkové kategorie tato pojišťovna nepojistí.
        while True:
            age = input("Zadejte věk (nebo napište 'cancel' pro zrušení): ")
            if age.lower() == 'cancel':
                print("Vkládání nového pojištěnce bylo zrušeno.")
                break
            if not self.validate_age(age):
                print("Zadejte věk v rozmezí 1 až 80. Opakujte zadání")
                continue
            break
        # Zadáme telefonní číslo které je zkontrolováno dle podmínek uvedených výše.
        while True:
            phone = input(
                "Zadejte mobilní telefonní číslo, volitelně včetně volacího znaku země bez + (nebo napište 'cancel' pro zrušení): ").strip()
            if phone.lower() == 'cancel':
                print("Vkládání nového pojištěnce bylo zrušeno.")
                break
            if not self.validate_phone(phone):
                print("Telefonní číslo nesmí být prázdné a kratší než 9 čísel. Opakujte zadání.")
                continue
            formatted_phone = self.normalize_phone_number(phone)
            break
        # Po zadání je uživatel informován, zda byl záznam uložen nebo ne.
        try:
            age = int(age)
            insured = InsuredPerson(name, surname, age, formatted_phone)
            self.agent.add_record(insured)
            print(f"Záznam pojištěnce {name} {surname} byl úspěšně zadán.")
        except ValueError:
            print("Požadované údaje nebyly zadány správně. Opakujte zadání")

    # toto je hlavní ovládací rozhraní - nabídka - pro práci s pojištěnci

#class UserInterface:
    def main_loop(self):
        while True:
            print("----------------------")
            print("Evidence pojištěných")
            print("----------------------")
            print("Vyberte si akci:")
            print("1 - Přidat nového pojištěného")
            print("2 - Vypsat všechny pojištěné")
            print("3 - Vyhledat pojištěného")
            print("4 - Exportovat databázi")
            print("5 - Konec")
            choice = input()

            if choice == "1":
                self.get_user_input()
            elif choice == "2":
                self.agent.show_insured()
            elif choice == "3":
                if not self.agent.insured_list:
                    print("Databáze je prázdná. Prosím, nejdříve zadejte nějakého pojištěnce.")
                    continue
                name = input("Zadejte jméno: ").strip().capitalize()
                if not self.validate_name(name):
                    print("Jméno smí obsahovat pouze písmena. Opakujte zadání.")
                    continue
                surname = input("Zadejte příjmení: ").strip().capitalize()
                if not self.validate_surname(surname):
                    print("Příjmení smí obsahovat pouze písmena. Opakujte zadání.")
                    continue
                insured = self.agent.search_insured(name, surname)
                if insured:
                    print(f"{name} {surname} je pojištěn/a.")
                else:
                    print(f"Osobu se jméneme {name} a příjmením {surname} se nepodařilo nalézt.")
            elif choice == "4":
                filename = input("Zadejte název souboru k exportu (např. 'databáze.csv'): ")
                self.agent.export_database(filename)
            elif choice == "5":
                break
            else:
                print("Tato možnost neexistuje, zkuste to znovu")
