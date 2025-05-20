import os
import shutil
import re
import PySimpleGUI as sg
from pathlib import Path

def extract_author_and_series(filename):
    # Verwijder extensie en splits op streepjes
    name = Path(filename).stem
    parts = re.split(r'\s*-\s*', name)

    author = parts[0] if parts else "Unknown Author"
    title = parts[1] if len(parts) > 1 else "Unknown Title"
    
    # Zoek naar serie-info in titel (bijv. "Serie Naam 01")
    series_match = re.search(r'(.*?)(\s+(\d{1,3}))?$', title.strip())
    if series_match:
        series = series_match.group(1).strip()
        number = series_match.group(3) or "00"
    else:
        series = "Standalone"
        number = "00"

    return author.strip(), series.strip(), number.zfill(2)

def sort_books(source_folder, target_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.epub', '.pdf')):
                author, series, number = extract_author_and_series(file)
                series_folder = f"{series}"
                author_folder = os.path.join(target_folder, author)
                os.makedirs(author_folder, exist_ok=True)

                source_path = os.path.join(root, file)
                new_filename = f"{series} {number} - {Path(file).name}"
                target_path = os.path.join(author_folder, new_filename)

                # Bestanden met dezelfde naam overslaan
                if not os.path.exists(target_path):
                    shutil.copy2(source_path, target_path)

# GUI
layout = [
    [sg.Text('Source Folder:'), sg.InputText(key='SOURCE'), sg.FolderBrowse()],
    [sg.Text('Target Folder:'), sg.InputText(key='TARGET'), sg.FolderBrowse()],
    [sg.Button('Sort Books'), sg.Button('Exit')]
]

window = sg.Window('Book Sorter (Offline)', layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    if event == 'Sort Books':
        source = values['SOURCE']
        target = values['TARGET']
        if os.path.isdir(source) and os.path.isdir(target):
            sort_books(source, target)
            sg.popup('Sorting complete!', title='Done')
        else:
            sg.popup_error('Please select valid folders.')

window.close()
