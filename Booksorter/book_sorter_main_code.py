import os
import shutil

def is_fiction(file_name):
    keywords = ['roman', 'novel', 'thriller', 'fantasy', 'sci-fi', 'detective']
    return any(word.lower() in file_name.lower() for word in keywords)

def get_author(file_name):
    parts = file_name.split(' - ')
    if len(parts) > 1:
        return parts[0].strip()
    return "Unknown_Author"

def get_theme(file_name):
    parts = file_name.split(' - ')
    if len(parts) > 1:
        return parts[0].strip()
    return "General"

def organize_books(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith(('.pdf', '.epub', '.mobi')):
                full_path = os.path.join(root, file)

                if is_fiction(file):
                    author = get_author(file)
                    dest_folder = os.path.join(base_path, "Sorted_Fiction", author)
                else:
                    theme = get_theme(file)
                    dest_folder = os.path.join(base_path, "Sorted_NonFiction", theme)

                os.makedirs(dest_folder, exist_ok=True)
                dest_file = os.path.join(dest_folder, file)

                if not os.path.exists(dest_file):  # voorkom dubbele
                    shutil.move(full_path, dest_file)
                else:
                    print(f"Bestand al aanwezig: {file}")

if __name__ == "__main__":
    folder = input("Voer het pad in van de map met boeken: ")
    if os.path.isdir(folder):
        organize_books(folder)
        print("Boeken zijn gesorteerd in Fiction en Non-Fiction.")
    else:
        print("Ongeldig pad.")
