# Update for sorting audiobooks and saving book covers

updated_project_files = {
    "sort_books.py": '''import os
import shutil
import re
import hashlib
import json

bronmap = r"G:\\1. Boeken NL Fictie"
doelmap = r"G:\\1. Boeken NL Fictie sorted"
series_db_path = "series_db.json"

# Laad de series-database
try:
    with open(series_db_path, "r", encoding="utf-8") as f:
        series_db = json.load(f)
except FileNotFoundError:
    series_db = {}

os.makedirs(doelmap, exist_ok=True)

def splits_bestandsnaam(naam, auteur, series_db):
    naam_zonder_ext = os.path.splitext(naam)[0]
    ext = os.path.splitext(naam)[1]

    serie_match = re.search(r"\\[(.*?)\\s+(\\d+)\\]", naam_zonder_ext)
    if serie_match:
        serie = serie_match.group(1).strip()
        nummer = serie_match.group(2).zfill(2)
        serienaam = f"[{serie} {nummer}]"
        naam_zonder_ext = re.sub(r"\\[.*?\\]", "", naam_zonder_ext).strip()
    else:
        serienaam = ""

    delen = re.split(r"\\s*-\\s*", naam_zonder_ext, maxsplit=1)
    if len(delen) == 2:
        auteur_bestand, titel = delen
        if not auteur:
            auteur = auteur_bestand
    else:
        titel = naam_zonder_ext

    # Controleer op bekende series
    if auteur in series_db:
        for bekende_titel, serieinfo in series_db[auteur].items():
            if bekende_titel.lower() in titel.lower():
                serienaam = f"[{serieinfo}]"
                break

    nieuwe_bestandsnaam = f"{serienaam} {titel.strip()}{ext}".strip()
    return auteur.strip() if auteur else "Onbekend", nieuwe_bestandsnaam

def bereken_hash(pad):
    hasher = hashlib.sha256()
    with open(pad, "rb") as bestand:
        for blok in iter(lambda: bestand.read(4096), b""):
            hasher.update(blok)
    return hasher.hexdigest()

bekende_hashes = set()

for root, _, files in os.walk(bronmap):
    for naam in files:
        if not naam.lower().endswith(('.epub', '.pdf', '.mobi', '.mp3', '.m4b')):
            continue

        pad = os.path.join(root, naam)
        bestand_hash = bereken_hash(pad)
        if bestand_hash in bekende_hashes:
            print(f"❌ Dubbel verwijderd: {pad}")
            os.remove(pad)
            continue
        bekende_hashes.add(bestand_hash)

        auteur, nieuwe_bestandsnaam = splits_bestandsnaam(naam, None, series_db)
        mapnaam = os.path.join(doelmap, auteur)
        os.makedirs(mapnaam, exist_ok=True)

        doelpad = os.path.join(mapnaam, nieuwe_bestandsnaam)

        teller = 1
        origineel_doelpad = doelpad
        while os.path.exists(doelpad):
            doelpad = os.path.join(mapnaam, f"{os.path.splitext(nieuwe_bestandsnaam)[0]} ({teller}){os.path.splitext(nieuwe_bestandsnaam)[1]}")
            teller += 1

        shutil.move(pad, doelpad)
        print(f"✅ Verplaatst: {doelpad}")

        # Check and copy covers (if they exist in the same directory)
        for cover_ext in ['.jpg', '.png']:
            cover_file = os.path.join(root, naam.split('.')[0] + cover_ext)
            if os.path.exists(cover_file):
                cover_dest = os.path.join(mapnaam, naam.split('.')[0] + cover_ext)
                shutil.copy(cover_file, cover_dest)
                print(f"📸 Cover gekopieerd: {cover_dest}")
''',

