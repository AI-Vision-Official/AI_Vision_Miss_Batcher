
import tkinter as tk
import os
import hashlib
import sys
import os
import hashlib
import shutil
from PyQt5.QtWidgets import QTextEdit, QFileDialog


# Hulp: Dubbele bestanden verwijderen (via bestandsinhoud hash)
def remove_duplicates(folder):
    hashes = set()
    for filepath in glob.glob(folder + '/**/*', recursive=True):
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                filehash = hashlib.md5(f.read()).hexdigest()
            if filehash in hashes:
                os.remove(filepath)
            else:
                hashes.add(filehash)

# Hulp: Zoek boekinfo via OpenLibrary API
def fetch_book_info(title):
    url = f"https://openlibrary.org/search.json?q={title}"
    try:
        r = requests.get(url)
        data = r.json()
        if data['docs']:
            doc = data['docs'][0]
            return f"{doc.get('title')} by {doc.get('author_name', ['Unknown'])[0]}"
        return "No data found"
    except Exception as e:
        return f"Error: {e}"

# Sorteerfunctie
def sort_books(folder):
    output = []
    if not folder:
        return ["No folder selected."]
    
    remove_duplicates(folder)
    output.append("Removed duplicate files.")

    for filepath in glob.glob(folder + '/**/*.pdf', recursive=True):
        filename = os.path.basename(filepath)
        name = filename.rsplit('.', 1)[0]
        
        # Basis scheiding
        if "Fictie" in folder:
            key = name.split(" ")[-1]  # Laatste woord = auteur?
            subfolder = os.path.join(folder, "Sorted_By_Author", key)
        elif "Non" in folder:
            key = name.split(" ")[0]  # Eerste woord = thema?
            subfolder = os.path.join(folder, "Sorted_By_Theme", key)
        else:
            key = "Unknown"
            subfolder = os.path.join(folder, "Unsorted")
        
        os.makedirs(subfolder, exist_ok=True)
        try:
            shutil.move(filepath, os.path.join(subfolder, filename))
            info = fetch_book_info(name)
            output.append(f"Moved: {filename} → {subfolder} | Info: {info}")
        except Exception as e:
            output.append(f"Error moving {filename}: {e}")
    
    return output

# GUI Class
class BookSorterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Sorter by Brigitte")
        self.setGeometry(100, 100, 700, 400)

        # Futuristisch paars thema
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 0, 60))
        palette.setColor(QPalette.WindowText, QColor(220, 200, 255))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        
        self.label = QLabel("Select your folder to sort:")
        self.layout.addWidget(self.label)
        
        self.button = QPushButton("Choose Folder")
        self.button.clicked.connect(self.choose_folder)
        self.layout.addWidget(self.button)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.layout.addWidget(self.output_box)

        self.setLayout(self.layout)
        self.folder_path = None

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.output_box.append(f"Selected: {folder}")
            result = sort_books(folder)
            for line in result:
                self.output_box.append(line)

# Start de GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookSorterApp()
    window.show()
    sys.exit(app.exec_())
