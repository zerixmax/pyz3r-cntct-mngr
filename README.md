# 🐍 pyz3r-cntct-mngr

**Contact Manager** - Python konzolna aplikacija za upravljanje kontaktima i firmama

---

## 📋 O projektu

Aplikacija razvijena u sklopu **Python Developer** tečaja na **Algebra** veleučilištu.
Omogućuje sigurno upravljanje kontaktima kroz login sustav i intuitivno sučelje.

## ✨ Funkcionalnosti

### 🔐 Sigurnost
- **Login sustav** s ograničenim pokušajima prijave
- Provjera korisničkih podataka prije pristupa

### 👥 Upravljanje kontaktima
- Prikaz svih kontakata (tablični format)
- Prikaz kontakata po firmi
- Dodavanje novih kontakata
- Ažuriranje postojećih kontakata

### 🏢 Upravljanje firmama
- Dodavanje novih firmi
- Ažuriranje podataka firmi
- Jedinstveni OIB za svaku firmu

### ✅ Validacija podataka
- Email format provjera
- OIB jedinstvenost
- Potvrda prije važnih akcija

## 🚀 Pokretanje


🔐 Login sustav (iz fleet managera)
✅ Lista korisnika s username/password

✅ Funkcija login() s ograničenjem na 3 pokušaja

✅ Provjera prije pristupa glavnom meniju

✅ Profesionalan UX s čišćenjem ekrana

📊 Struktura podataka (prema zahtjevima)
✅ Kontakt model: id, name, surname, phone, email

✅ Firma model: id, name, vat_id, contacts (lista ID-ova)

✅ Pravilne veze između firmi i kontakata

⚙️ Kompletne funkcionalnosti
✅ Prikaz svih kontakata (tablični format)

✅ Prikaz kontakata po firmi

✅ Dodavanje firme/kontakta s validacijom

✅ Ažuriranje firme/kontakta

✅ Email format validacija

✅ Jedinstveni OIB provjera
