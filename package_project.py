"""
Package the entire project into a clean, ready-to-submit ZIP archive.
"""

import zipfile
import os

ZIP_NAME = "EV_Charging_Load_Impact_Simulator.zip"
EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode", ".agents", "scratch"}
EXCLUDE_EXTS = {".pyc", ".DS_Store"}

def make_zip():
    print(f"Creating submission archive: {ZIP_NAME}...")
    total_files = 0
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
            for file in files:
                if file == ZIP_NAME or any(file.endswith(ext) for ext in EXCLUDE_EXTS) or file.startswith("."):
                    continue
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, ".")
                zf.write(file_path, archive_name)
                total_files += 1

    size_mb = os.path.getsize(ZIP_NAME) / (1024 * 1024)
    print(f"Archive successfully created! Contains {total_files} files ({size_mb:.2f} MB).")

if __name__ == "__main__":
    make_zip()
