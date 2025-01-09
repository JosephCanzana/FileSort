import os
import shutil
import time

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

# Downloads folder path
# Add your path MacOs: /Users/YourName/Downloads
# Add your path Linux: /home/yourname/downloads
# Add your path Windows Linux WSL: /mnt/c/User/yourname/Downloads
# Add your path Windows: C:\Users\YourName\Downloads
my_downloads_path = "" 

def main():
    # Initial sorting of existing files
        for file in os.listdir(my_downloads_path):
            file_path = os.path.join(my_downloads_path, file)
            if os.path.isfile(file_path) and is_file_fully_downloaded(file_path, wait_time=2):
                sort_files(file_path)

        # Start polling-based monitoring
        monitor_and_sort(polling_interval=2, download_wait_time=2)


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
    file_name = os.path.basename(file_path)  # Get only the file name
    file_extension = os.path.splitext(file_name)[1].lower()

    # Check the extension against the dictionary
    for folder, extensions in file_type_folders.items():
        if file_extension in extensions:
            folder_path = os.path.join(my_downloads_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"File: {file_name} to Folder: {folder_path}")
            shutil.move(file_path, os.path.join(folder_path, file_name))
            return
        
    # Move to "Others" if no match
    folder_path = os.path.join(my_downloads_path, "Others")
    os.makedirs(folder_path, exist_ok=True)
    shutil.move(file_path, os.path.join(folder_path, file_name))


# Function to poll for changes in the directory
def monitor_and_sort(polling_interval=2, download_wait_time=2):
    print(f"Monitoring {my_downloads_path}... Press Ctrl+C to stop.")
    previously_seen = set(os.listdir(my_downloads_path))

    try:
        while True:
            time.sleep(polling_interval)
            current_files = set(os.listdir(my_downloads_path))
            
            # Detect newly added files
            new_files = current_files - previously_seen
            for file in new_files:
                file_path = os.path.join(my_downloads_path, file)
                if os.path.isfile(file_path):
                    print(f"New file detected: {file}")
                    if is_file_fully_downloaded(file_path, wait_time=download_wait_time):
                        sort_files(file_path)
                    else:
                        print(f"File {file} is still being downloaded, skipping this cycle.")
            
            # Update the state of previously seen files
            previously_seen = current_files

    except KeyboardInterrupt:
        print("Stopped monitoring.")


if __name__ == "__main__":
    main()
