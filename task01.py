from pathlib import Path
import shutil
import argparse
import os

# Constants
ACCESS_MODE = os.R_OK | os.W_OK | os.X_OK

def copy_files(source, destination):
    """
    Recursively copies files from the source directory to the destination directory.
    """
    destination.mkdir(parents=True, exist_ok=True)

    for current_path in source.iterdir():
        if current_path.is_dir():
            copy_files(current_path, destination)
        else:
            has_access = check_access(current_path)
            if has_access:
                destination_folder = create_folder_by_extension(current_path, destination)
                if destination_folder:
                    copy_path = check_duplicates(current_path, destination_folder)
                    shutil.copy(current_path, copy_path)


def create_folder_by_extension(file_path, destination_folder):
    """
    Creates a folder based on the file extension in the destination folder.
    """
    file_extension = file_path.suffix.lower()

    if file_extension:
        folder_path = destination_folder.joinpath(file_extension[1:])
        folder_path.mkdir(parents=True, exist_ok=True)
        return folder_path

    return None


def check_access(file_path):
    """
    Checks if the script has read, write, and execute access to a file.
    """
    try:
        os.access(file_path, ACCESS_MODE)
        return True
    except PermissionError as e:
        print(f"No access rights for {file_path}: {e}")
        return False


def check_duplicates(file_path, destination_folder):
    """
    Checks for duplicate files in the destination folder and generates a unique copy path.
    """
    file_name = file_path.stem
    file_extension = file_path.suffix

    copy_path = destination_folder / f"{file_name}{file_extension}"

    index = 1
    while copy_path.exists():
        unique_name = f"{file_name}_copy_{index}"
        copy_path = destination_folder / f"{unique_name}{file_extension}"
        index += 1

    return copy_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copying files")

    parser.add_argument(
        "--source",
        default=Path.cwd(),
        type=Path,
        help="The path to the source directory",
        required=False,
    )
    parser.add_argument(
        "--destination",
        default=Path("./dist"),
        type=Path,
        help="The path to the destination directory",
        required=False,
    )

    args = parser.parse_args()

    copy_files(args.source, args.destination)
    print("Copying complete")
