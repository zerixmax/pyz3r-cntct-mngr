# ░█▀█░█░█░▀▀█░▀▀█░█▀▄
# ░█▀▀░░█░░▄▀░░░▀▄░█▀▄
# ░▀░░░░▀░░▀▀▀░▀▀░░▀░▀
import re
import sys

import os
#region MODELI
korisnici = [
    {
        'id': 1,
        'first_name': 'Admin',
        'last_name': 'User',
        'username': 'admin',
        'password': '123'
    }
]

kontakti = {} # key: id, value: kontakt dict
firme = {}   # key: id, value: firma dict

#endregion

#region FUNKCIJE

def is_valid_email(email):
    """Provjerava je li email adresa u ispravnom formatu."""
    if not email: return False
    # Jednostavan regex za provjeru formata emaila
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_oib(oib):
    """Provjerava je li OIB u ispravnom formatu (11 znamenki)."""
    if not oib: return False
    return len(oib) == 11 and oib.isdigit()

def dodaj_firmu(id, name, vat_id):
    firma = {
        'id': id,
        'name': name,
        'vat_id': vat_id,
        'contacts': []  # Inicijaliziraj listu kontakata za firmu
    }
    firme[id] = firma

def dodaj_kontakt(id, name, surname, phone, email, company_id=None):
    kontakt = {
        'id': id,
        'name': name,
        'surname': surname,
        'phone': phone,
        'email': email
    }
    kontakti[id] = kontakt
    if company_id is not None and company_id in firme:
        firme[company_id]['contacts'].append(id)
    
def prikaz_svih_kontakata(puni_prikaz=True):
    if puni_prikaz:
        print("--- Svi kontakti ---")
        print("-" * 90)
        print(f"{'ID':<5} | {'Ime i Prezime':<25} | {'Telefon':<15} | {'Email':<25} | {'Firma':<15}")
        print("-" * 90)

    if not kontakti:
        print("Nema unesenih kontakata.")
        return

    for kontakt_id, k in kontakti.items():
        # Pronađi firmu za dani kontakt
        naziv_firme = "Nije dodijeljen"
        for firma_id, firma_data in firme.items():
            if kontakt_id in firma_data['contacts']:
                naziv_firme = firma_data['name']
                break
        puno_ime = f"{k['name']} {k['surname']}"
        print(f"{k['id']:<5} | {puno_ime:<25} | {k['phone']:<15} | {k['email']:<25} | {naziv_firme:<15}")
    if puni_prikaz:
        print("-" * 90)

def show_company_contacts(company_id):
    if company_id in firme:
        firma = firme[company_id]
        print(f"Svi kontakti za firmu {firme[company_id]['name']}:")
        print("-" * 70)
        print(f"{'ID':<5} | {'Ime i Prezime':<25} | {'Telefon':<15} | {'Email':<25}")
        print("-" * 70)
        if not firma['contacts']:
            print("  Ova firma nema dodijeljenih kontakata.")
        else:
            for kid in firma['contacts']:
                if kid in kontakti:
                    k = kontakti[kid]
                    puno_ime = f"{k['name']} {k['surname']}"
                    print(f"{k['id']:<5} | {puno_ime:<25} | {k['phone']:<15} | {k['email']:<25}")
        print("-" * 70)
    else:
        print(f"Firma s ID {company_id} ne postoji.")

def prikaz_svih_firmi():
    print("--- Sve firme ---")
    print(f"{'ID':<5} | {'Naziv':<25} | {'OIB':<15} | {'Br. kontakata':<15}")
    print("-" * 70)
    for fid, firma in firme.items():
        broj_kontakata = len(firma['contacts'])
        print(f"{fid:<5} | {firma['name']:<25} | {firma['vat_id']:<15} | {broj_kontakata:<15}")
    print("-" * 70)


def update_company(id, name=None, vat_id=None):
    if id in firme:
        if name is not None:
            firme[id]['name'] = name
        if vat_id is not None:
            firme[id]['vat_id'] = vat_id

def update_contact(id, name=None, surname=None, phone=None, email=None, company_id=None):
    if id in kontakti:
        if name is not None:
            kontakti[id]['name'] = name
        if surname is not None:
            kontakti[id]['surname'] = surname
        if phone is not None:
            kontakti[id]['phone'] = phone
        if email is not None:
            kontakti[id]['email'] = email
        if company_id is not None:
            # Pronađi staru firmu i ukloni kontakt iz nje
            stari_company_id = None
            for fid, f in firme.items():
                if id in f['contacts']:
                    stari_company_id = fid
                    break
            
            # Ukloni kontakt iz liste kontakata stare firme
            if stari_company_id in firme and id in firme[stari_company_id]['contacts']:
                firme[stari_company_id]['contacts'].remove(id)
            
            # Dodaj kontakt u listu kontakata nove firme
            if company_id in firme:
                firme[company_id]['contacts'].append(id)

def delete_contact(contact_id):
    """Briše kontakt iz sustava."""
    if contact_id not in kontakti:
        return False

    # Ukloni kontakt iz rječnika kontakata
    del kontakti[contact_id]

    # Ukloni referencu na kontakt iz svih firmi
    for firma_id in firme:
        if contact_id in firme[firma_id]['contacts']:
            firme[firma_id]['contacts'].remove(contact_id)
            break  # Kontakt može biti samo u jednoj firmi
    return True

def delete_company(company_id):
    """Briše firmu i sve njezine kontakte."""
    if company_id not in firme:
        return False

    # Prvo obriši sve kontakte povezane s firmom
    contact_ids_to_delete = list(firme[company_id]['contacts'])
    for contact_id in contact_ids_to_delete:
        if contact_id in kontakti:
            del kontakti[contact_id]
    
    del firme[company_id]
    return True

def login(max_attempts=3):
    """Funkcija za prijavu korisnika s ograničenim brojem pokušaja."""
    for attempt in range(max_attempts):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\tPy Kontakt Manager - Prijava korisnika")
        print("="*50)
        print(f"Pokušaj {attempt + 1} od {max_attempts}")
        username = input('Unesite korisničko ime: ').strip()
        password = input('Unesite lozinku: ').strip()

        for korisnik in korisnici:
            if username.lower() == korisnik['username'].lower() and password == korisnik['password']:
                print(f"\nPrijava uspješna. Dobrodošao, {korisnik['first_name']} {korisnik['last_name']}!")
                input("Pritisnite ENTER za ulazak u aplikaciju...")
                return korisnik
        
        print("\nNetočno korisničko ime ili lozinka.")
        if attempt < max_attempts - 1:
            input("Pritisnite ENTER za ponovni unos...")
    
    print("\nPrekoračili ste broj dopuštenih pokušaja.")
    input("Pritisnite ENTER za izlaz iz programa...")
    return None
        
#endregion

#region Main
if __name__  ==  '__main__':
    # --- Inicijalizacija s testnim podacima ---
    dodaj_firmu(1, 'Firma A', '12345678901')
    dodaj_firmu(2, 'Firma B', '98765432101')
    dodaj_kontakt(1, 'Pero', 'Peric', '0912345678', 'pero.peric@example.com', 1)
    dodaj_kontakt(2, 'Ana', 'Anic', '0987654321', 'ana.anic@example.com', 1)

    prijavljeni_korisnik = login()

    if not prijavljeni_korisnik:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Prijava neuspješna. Program se završava.")
        sys.exit()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\tPy Kontakt Manager - Glavni izbornik")
        print("="*50)
        print(f"Prijavljeni korisnik: {prijavljeni_korisnik['first_name']} {prijavljeni_korisnik['last_name']}")
        print("-" * 50)
        print("1. Prikaz svih kontakata")
        print("2. Prikaz kontakata po firmi")
        print("3. Dodaj novi kontakt")
        print("4. Dodaj novu firmu")
        print("5. Ažuriraj kontakt")
        print("6. Ažuriraj firmu")
        print("7. Prikaz svih firmi")
        print("8. Obriši kontakt")
        print("9. Obriši firmu")
        # Ovdje se mogu dodati i druge opcije (ažuriranje firme, brisanje...)
        print("0. Izlaz")
        print("="*50)

        izbor = input("Odaberite opciju: ")

        if izbor == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            prikaz_svih_kontakata()
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- Prikaz kontakata po firmi ---")
            for firma_id, firma_data in firme.items():
                print(f"ID: {firma_id} - {firma_data['name']}")
            try:
                firma_id_izbor = int(input("\nUnesite ID firme za prikaz kontakata: "))
                print("-" * 30)
                show_company_contacts(firma_id_izbor)
            except ValueError:
                print("Pogrešan unos. Molimo unesite broj.")
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- Dodavanje novog kontakta ---")
            novi_id = max(kontakti.keys()) + 1 if kontakti else 1
            ime = input("Unesite ime: ")
            prezime = input("Unesite prezime: ")
            telefon = input("Unesite telefon: ")
            while True:
                email = input("Unesite email: ")
                if is_valid_email(email):
                    break
                print("Neispravan format email adrese. Pokušajte ponovo.")

            try:
                firma_id = int(input("Unesite ID firme kojoj pripada kontakt: "))
                if firma_id not in firme:
                    print(f"Firma s ID-om {firma_id} ne postoji. Kontakt nije dodan.")
                else:
                    potvrda = input(f"Jeste li sigurni da želite dodati kontakt '{ime} {prezime}'? (da/ne): ").lower()
                    if potvrda == 'da':
                        dodaj_kontakt(novi_id, ime, prezime, telefon, email, company_id=firma_id)
                        print("\nKontakt uspješno dodan!")
                    else:
                        print("\nDodavanje otkazano.")
            except ValueError:
                print("Pogrešan unos za ID firme. Molimo unesite broj.")
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- Dodavanje nove firme ---")
            novi_id = max(firme.keys()) + 1 if firme else 1
            naziv = input("Unesite naziv firme: ")
            while True:
                oib = input("Unesite OIB firme: ")
                if not is_valid_oib(oib):
                    print("Neispravan format OIB-a. OIB mora imati 11 znamenki.")
                elif any(f['vat_id'] == oib for f in firme.values()):
                    print("Firma s ovim OIB-om već postoji. Pokušajte ponovo.")
                else:
                    break
            
            potvrda = input(f"Jeste li sigurni da želite dodati firmu '{naziv}'? (da/ne): ").lower()
            if potvrda == 'da':
                dodaj_firmu(novi_id, naziv, oib)
                print("\nFirma uspješno dodana!")
            else:
                print("\nDodavanje otkazano.")
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- Ažuriranje kontakta ---")
            prikaz_svih_kontakata(puni_prikaz=False)
            try:
                kontakt_id = int(input("\nUnesite ID kontakta za ažuriranje: "))
                if kontakt_id not in kontakti:
                    print("Kontakt s tim ID-om ne postoji.")
                else:
                    print(f"Unesite nove podatke za kontakt ID: {kontakt_id} (ostavite prazno ako ne želite promjenu)")
                    ime = input(f"Ime [{kontakti[kontakt_id]['name']}]: ") or None
                    prezime = input(f"Prezime [{kontakti[kontakt_id]['surname']}]: ") or None
                    telefon = input(f"Telefon [{kontakti[kontakt_id]['phone']}]: ") or None
                    email = input(f"Email [{kontakti[kontakt_id]['email']}]: ") or None
                    if email and not is_valid_email(email):
                        print("Neispravan format email adrese. Ažuriranje prekinuto.")
                    else:
                        potvrda = input("Jeste li sigurni da želite spremiti izmjene? (da/ne): ").lower()
                        if potvrda == 'da':
                            update_contact(kontakt_id, name=ime, surname=prezime, phone=telefon, email=email)
                            print("\nKontakt uspješno ažuriran!")
                        else:
                            print("\nAžuriranje otkazano.")
            except ValueError:
                print("Pogrešan unos. Molimo unesite broj.")
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '6':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- Ažuriranje firme ---")
            for firma_id, firma_data in firme.items():
                print(f"ID: {firma_id} - {firma_data['name']}")
            try:
                firma_id_izbor = int(input("\nUnesite ID firme za ažuriranje: "))
                if firma_id_izbor not in firme:
                    print("Firma s tim ID-om ne postoji.")
                else:
                    print(f"Unesite nove podatke za firmu ID: {firma_id_izbor} (ostavite prazno ako ne želite promjenu)")
                    naziv = input(f"Naziv [{firme[firma_id_izbor]['name']}]: ") or None
                    oib_input = input(f"OIB [{firme[firma_id_izbor]['vat_id']}]: ")
                    oib = oib_input if oib_input else None

                    if oib and not is_valid_oib(oib):
                        print("Neispravan format OIB-a. Ažuriranje prekinuto.")
                    else:
                        potvrda = input("Jeste li sigurni da želite spremiti izmjene? (da/ne): ").lower()
                        if potvrda == 'da':
                            update_company(firma_id_izbor, name=naziv, vat_id=oib)
                            print("\nFirma uspješno ažurirana!")
                        else:
                            print("\nAžuriranje otkazano.")
            except ValueError:
                print("Pogrešan unos. Molimo unesite broj.")
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            prikaz_svih_firmi()
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '8':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- Brisanje kontakta ---")
            prikaz_svih_kontakata(puni_prikaz=False)
            try:
                kontakt_id = int(input("\nUnesite ID kontakta za brisanje: "))
                if kontakt_id not in kontakti:
                    print("Kontakt s tim ID-om ne postoji.")
                else:
                    potvrda = input(f"Jeste li sigurni da želite obrisati kontakt '{kontakti[kontakt_id]['name']}'? (da/ne): ").lower()
                    if potvrda == 'da':
                        if delete_contact(kontakt_id):
                            print("\nKontakt uspješno obrisan!")
                        else:
                            print("\nBrisanje nije uspjelo.")
                    else:
                        print("\nBrisanje otkazano.")
            except ValueError:
                print("Pogrešan unos. Molimo unesite broj.")
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '9':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- Brisanje firme ---")
            prikaz_svih_firmi()
            try:
                firma_id_izbor = int(input("\nUnesite ID firme za brisanje: "))
                if firma_id_izbor not in firme:
                    print("Firma s tim ID-om ne postoji.")
                else:
                    potvrda = input(f"UPOZORENJE: Brisanje firme '{firme[firma_id_izbor]['name']}' obrisat će i sve njezine kontakte.\nJeste li sigurni? (da/ne): ").lower()
                    if potvrda == 'da' and delete_company(firma_id_izbor):
                        print("\nFirma i svi njezini kontakti su uspješno obrisani.")
                    else:
                        print("\nBrisanje otkazano.")
            except ValueError:
                print("Pogrešan unos. Molimo unesite broj.")
            input("\nPritisnite ENTER za povratak na izbornik...")

        elif izbor == '0':
            print("\nHvala na korištenju. Doviđenja!")
            break

#endregion