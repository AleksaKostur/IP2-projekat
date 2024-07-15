# FP-Tree Constructor

Ovaj projekat predstavlja implementaciju algoritma FP-rasta za generisanje FP-drveta i pronalaženje čestih skupova stavki. Rad predstavlja projekat iz predmeta Istraživanje podataka 2 na Matematičkom fakultetu u Beogradu.

## Instalacija

Da biste pokrenuli ovaj projekat, potrebno je da imate Python instaliran na vašem računaru. Takođe, potrebno je da instalirate sledeće Python biblioteke:

- pyfpgrowth
- networkx
- matplotlib
- tkinter

Možete ih instalirati koristeći pip:

```bash
pip install pyfpgrowth networkx matplotlib tk
```

## Korišćenje

Pozicionirajte se u direktorium gde se sačuvali fajl FP-drvo.py i pokrenite komandu:
```bash
python FP-drvo.py
```

Prvi korak u korišćenju programa je unošenje liste transakcija. Transakcije se mogu uneti na dva načina: klikom na dugme „Učitaj transakcije“ ili direktnim unosom u tekstualno polje. Svaka transakcija mora da se nalazi u novom redu, stavke u transakciji moraju biti razdvojene razmakom.
Nakon unetih transakcija, klikom na dugme „Nacrtaj FP-drvo“, program iscrtava FP-drvo. Ukoliko ne postoji unos u tekstualnom polju, program će izbaciti obaveštenje o grešci. 
Slika se može sačuvati na disku klikom na dugme „Sačuvaj sliku“. Podrazumevani format za čuvanje slike je Portable Network Graphics (.png). Ukoliko ne postoji slika FP-drveta, program će izbaciti obaveštenje o grešci. 

Drugi korak u korišćenju programa je unošenje minimalne podrške. Minimalna podrška mora biti pozitivan ceo broj. 
Nakon unete minimalne podrške, klikom na dugme „Odredi česte skupove stavki“, program ispisuje česte skupove stavki u tekstualno polje ispod. Ukoliko ne postoji unos transakcija ili minimalne podrške, program izbacuje obaveštenje o grešci. Takođe, ukoliko minimalna podrška nije pozitivan ceo broj, program takođe izbacuje obaveštenje o grešci.
Česti skupovi stavki se mogu sačuvati na disku klikom na dugme „Sačuvaj česte skupove stavki“. Podrazumevani format za čuvanje teksta je Text File (.txt). Ukoliko ne postoji nikakav tekst, program će izbaciti obaveštenje o grešci. 
