1. Bewerk het bestand "series_db.json" om je eigen series in te voeren.
   Voorbeeld:
   {
     "Auteur Naam": {
       "Boektitel": "SerieNaam 01",
       "Andere Titel": "SerieNaam 02"
     }
   }

2. Zet het script en JSON-bestand naast elkaar.

3. Start het script vanuit Python 3.13 of hoger.

4. Bestanden worden uit G:\\1. Boeken NL Fictie gehaald
   en verplaatst naar G:\\1. Boeken NL Fictie sorted, gesorteerd per auteur en serie.

5. Audioboeken (.mp3, .m4b) worden ook verplaatst.

6. Covers van boeken (.jpg, .png) worden meegenomen en opgeslagen.

Veel succes Brigitte! 😊
'''
}

# Schrijf naar ZIP-bestand
updated_zip_pad = "/mnt/data/Boekensorteerder_met_audioboeken_en_covers.zip"
with zipfile.ZipFile(updated_zip_pad, 'w') as zipf:
    for bestandsnaam, inhoud in updated_project_files.items():
        zipf.writestr(bestandsnaam, inhoud)