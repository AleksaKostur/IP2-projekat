# IP2-projekat
Projekat iz predmeta Istraživanje podataka 2 na Matematičkom fakultetu u Beogradu.

# FP-Tree Constructor

Ovaj projekat predstavlja implementaciju algoritma FP-rasta za generisanje FP-drveta i pronalaženje čestih skupova stavki.

## Instalacija

Da biste pokrenuli ovaj projekat, potrebno je da imate Python instaliran na vašem računaru. Takođe, potrebno je da instalirate sledeće Python biblioteke:

- pyfpgrowth
- networkx
- matplotlib
- tkinter

Možete ih instalirati koristeći pip:

```bash
pip install pyfpgrowth networkx matplotlib tkinter
```

## Korišćenje

Pozicionirajte se u direktorium gde se sačuvali fajl FP-drvo.py i pokrenite komandu (komanda važi za OS Windows)
```bash
python .\FP-drvo.py
```
Unesite transakcije (svaka transakcija u novom redu, stavke između razdvojene razmakom) i minimalnu podršku, a zatim kliknite na “Nacrtaj FP-drvo” da biste generisali FP-drvo. Kliknite na “Odredi česte skupove stavki” da biste pronašli česte skupove stavki. Možete sačuvati sliku FP-drva klikom na “Sačuvaj sliku”.
