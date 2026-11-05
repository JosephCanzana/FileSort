import os
import shutil
import sys
import subprocess
import time
from pathlib import Path

# Define the file type folders
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

PARTIAL_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}

# Download path
my_downloads_path = Path.home()/"Downloads"

def main():
    if "--uninstall" in sys.argv[1:]:
        uninstall()
        return

    moved = 0    
    # Initial sorting of existing files
    for file in os.listdir(my_downloads_path):
        if os.path.splitext(file)[1].lower() in PARTIAL_EXTENSIONS:
            continue
        file_path = os.path.join(my_downloads_path, file)
        if os.path.isfile(file_path) and is_file_fully_downloaded(file_path, wait_time=2):

            # Sort and increment value on the number of sorted values
            if sort_files(file_path):
                moved += 1

    if moved == 0:
        print("There's nothing to sort")
    else:
        print(f"Sorted {moved} file(s)")


# Function to check if the file is fully downloaded
def is_file_fully_downloaded(file_path, wait_time=2):
    """
    Checks if the file's size remains constant for a specified wait time (in seconds).
    """
    try:
        initial_size = os.path.getsize(file_path)
        time.sleep(wait_time)
        new_size = os.path.getsize(file_path)
        return initial_size == new_size
    except FileNotFoundError:
        # File might have been moved or deleted during the check
        return False


# Function to sort files
def sort_files(file_path):
    # Get only the file name
    file_name = os.path.basename(file_path)
    # File extension
    file_extension = os.path.splitext(file_name)[1].lower()

    # Check the extension against the dictionary
    for folder, extensions in file_type_folders.items():
        if file_extension in extensions:
            folder_path = os.path.join(my_downloads_path, folder)
            folder_path, file_name = unique_destination(folder_path, file_name)
            move_file(file_path, folder_path, file_name)
            return
        
    # Move to "Others" if no match
    folder_path = os.path.join(my_downloads_path, "Others")
    folder_path, file_name = unique_destination(folder_path, file_name)
    move_file(file_path, folder_path, file_name)

def move_file(file_path, folder_path, file_name):
    os.makedirs(folder_path, exist_ok=True)
    dest = os.path.join(folder_path, file_name)
    try:
        os.rename(file_path, dest)
        print(f"Moved: {file_name} -> {folder_path}")
    except PermissionError:
        print(f"Skipped (in use): {file_name}")
    except OSError as e:
        print(f"Skipped ({e}): {file_name}")


def unique_destination(folder_path, file):

    # path of file destination
    full_path = Path(os.path.join(folder_path, file))

    # disect folder path
    file_name = os.path.splitext(file)[0]
    file_extension = os.path.splitext(file)[1]

    # Loop until file is successfully renamed
    name_counter = 1
    while True:
        # file destination already exist
        if full_path.is_file():
            file = f"{file_name} ({name_counter}){file_extension}"
            full_path = Path(os.path.join(folder_path, file))
            name_counter += 1
        else:
            break

    return folder_path, file


def uninstall():
    uv_path = shutil.which("uv")
    if not uv_path:
        print("uv not found, run uv tool uninstall filesort manually")
        return
    
    while True:
        confirmation = input("Remove filesort? [y/n]")
        if confirmation == "y":
            result = subprocess.run([uv_path, "tool", "uninstall", "filesort"])
            if result.returncode == 0:
                print("filesort has been removed.")
            else:
                print("Uninstall failed. Try manually: uv tool uninstall filesort")
            break
        elif confirmation == "n":
            print("Uninstalling filesort is cancelled")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()