import os
import shutil

# Folder to organize
folder_path = input("Enter the folder path to organize: ")

# File type categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Audio": [".mp3", ".wav"]
}

# Check if folder exists
if not os.path.exists(folder_path):
    print("Folder does not exist.")
    exit()

# Scan files
files = os.listdir(folder_path)

for file in files:

    file_path = os.path.join(folder_path, file)

    # Skip directories
    if os.path.isdir(file_path):
        continue

    file_extension = os.path.splitext(file)[1].lower()

    moved = False

    for folder, extensions in file_types.items():
        if file_extension in extensions:

            target_folder = os.path.join(folder_path, folder)

            # Create folder if it doesn't exist
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            shutil.move(file_path, os.path.join(target_folder, file))
            moved = True
            break

    # If file type not recognized
    if not moved:
        other_folder = os.path.join(folder_path, "Others")

        if not os.path.exists(other_folder):
            os.makedirs(other_folder)

        shutil.move(file_path, os.path.join(other_folder, file))

print("✅ Files organized successfully!")