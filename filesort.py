import os
import shutil

# Folders
file_type_folders = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".tiff", ".webp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".csv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Programs": [".exe", ".msi", ".sh", ".bat", ".apk"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".php", ".ts", ".json"],
    "Others": []
}


downloads = "/mnt/c/Users/canza/Downloads"
os.makedirs(downloads, exist_ok=True)

print(f"Downloads: {downloads}")
# Get the file
files = os.listdir(downloads)
print(files)
for file in files:
    print(file)
    file_path = os.path.join(downloads,file)
    if os.path.isfile(file_path): 
        file_extension = os.path.splitext(file)[1].lower() 

        # Check the extension against the dictionary
        for folder, extensions in file_type_folders.items():
            if file_extension in extensions:

                # Check if folder path exist 
                folder_path = os.path.join(downloads, folder)
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)

                # Move the file using .move(source, destination)
                shutil.move(os.path.join(downloads, file), os.path.join(folder_path, file))
                break
        else:
            folder_path = os.path.join(downloads, "Others")
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                shutil.move(os.path.join(downloads, file), os.path.join(folder_path, file))