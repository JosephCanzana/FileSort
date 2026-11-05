# filesort

A small command-line tool that sorts your Downloads folder into subfolders by file type. Run `filesort` and files like `photo.png`, `report.pdf` and `song.mp3` are moved into `Images/`, `Documents/` and `Music/` inside your Downloads folder.

#### Video Demo: <URL HERE>

## Features

- Sorts every file in your Downloads folder into a category folder.
- Never overwrites: if `report.pdf` already exists in `Documents/`, the new file becomes `report (1).pdf`.
- Skips files that are still downloading (`.crdownload`, `.part`, `.tmp`, `.download`).
- Skips files that are in use by another program, and leaves them in Downloads for the next run.
- Works on Windows, macOS and Linux.
- Installs as a real `filesort` command you can run from any folder.

## Categories

| Folder | Extensions |
|---|---|
| Images | .jpg .jpeg .png .gif .bmp .svg .tiff .webp |
| Videos | .mp4 .mkv .avi .mov .wmv .flv .webm |
| Documents | .pdf .doc .docx .xls .xlsx .ppt .pptx .txt .csv |
| Music | .mp3 .wav .aac .flac .ogg .wma |
| Archives | .zip .rar .7z .tar .gz .bz2 |
| Programs | .exe .msi .sh .bat .apk |
| Code | .py .js .html .css .java .c .cpp .php .ts .json |
| Others | anything not listed above |

## Installation

You don't need to install Python first. The installer uses [uv](https://docs.astral.sh/uv/), installs it if it's missing, and uv downloads Python 3.12 automatically.

1. Download or clone this project and open a terminal in the project folder.
2. Run the installer for your system:

   **Linux / macOS**
   ```bash
   chmod +x install.sh   # only needed once
   ./install.sh
   ```

   **Windows (PowerShell)**
   ```powershell
   .\install.ps1
   ```
   If PowerShell blocks the script, run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install.ps1
   ```

3. Open a **new** terminal (so your PATH refreshes).

After installing, you can delete the project folder. The installed command keeps working.

## Usage

```bash
filesort              # sort your Downloads folder
filesort --uninstall  # remove filesort
```

filesort runs once and then exits. It does not watch the folder in the background, so run it again whenever you want to tidy up.

### Running without installing

If you just want to try it, you only need Python 3.12 or newer:

```bash
python filesort.py    # or python3 filesort.py
```

## Updating

Get the latest code and run the installer again. It reinstalls over the old version:

```bash
git pull
./install.sh          # or .\install.ps1 on Windows
```

## Uninstalling

```bash
filesort --uninstall
```

You'll be asked to confirm. This removes the `filesort` command only. It does not remove uv, and it does not move your sorted files back. If the command fails, you can always run this yourself:

```bash
uv tool uninstall filesort
```

## Project files

| File | Purpose |
|---|---|
| `filesort.py` | The program: sorting logic and the `--uninstall` option |
| `pyproject.toml` | Project info, and what creates the `filesort` command |
| `install.sh` | Installer for Linux and macOS |
| `install.ps1` | Installer for Windows |

## Design decisions

- **Extension map.** Files are matched by extension using a dictionary of folder names to extensions. It's simple to read and to extend, and anything unknown falls back to `Others` instead of being left behind.
- **Waiting for downloads to finish.** Before moving a file, filesort checks its size, waits 2 seconds, and checks again. If the size changed, the file is still being written, so it's skipped. Known partial-download extensions are skipped outright.
- **No overwriting.** Moving a file onto an existing name would silently destroy the old file on Linux/macOS, so filesort adds a counter, `name (1).ext`, `name (2).ext` and so on, until the name is free.
- **Moving with `os.rename`.** Every destination is a subfolder of Downloads, so a rename is enough. If a file is locked by another program, the rename fails cleanly and filesort skips it. `shutil.move` could copy the file and then fail to delete the original, which would leave duplicates.
- **A real command.** `pyproject.toml` defines the `filesort` entry point, and `uv tool install` installs the program into its own isolated environment. That's why it works from any folder and keeps working after the project folder is deleted.
- **Fixed Downloads location.** The folder is `~/Downloads` for the current user, so there's nothing to configure. I chose this to keep the tool simple and predictable.
- **Built-in uninstall.** The `--uninstall` option lives inside the program because the installer scripts may no longer exist after the user deletes the project folder.

## Limitations

- Only the top level of Downloads is sorted. Existing folders are left alone.
- Sorting is by extension only, so a file with no extension or a wrong one goes to `Others`.
- Files are never moved back automatically.