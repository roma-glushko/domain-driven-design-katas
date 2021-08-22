import hashlib
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Set


def hash_file(file_path: Path, block_size: int = 65536) -> str:
    hasher = hashlib.sha1()

    with open(file_path, "rb") as file:
        block = file.read(block_size)
        while block:
            hasher.update(block)
            block = file.read(block_size)

        return hasher.hexdigest()


def sync(source_path: str, destination_path: str):
    source_directory = Path(source_path)
    destination_directory = Path(destination_path)
    source_files_hashes: Dict[str, str] = {}

    for dir_path, _, file_names in os.walk(source_directory):
        for file_name in file_names:
            file_path: Path = Path(dir_path) / file_name

            source_files_hashes[hash_file(file_path)] = file_name

    destination_files_hashes: Set[str] = set()

    for dir_path, _, file_names in os.walk(destination_directory):
        for file_name in file_names:
            file_path: Path = Path(dir_path) / file_name
            file_hash = hash_file(file_path)

            destination_files_hashes.add(file_hash)

            if file_hash not in source_files_hashes:
                # file should be removed as it doesn't exist in the source directory
                file_path.remove()
                continue

            if (
                file_hash in source_files_hashes
                and source_files_hashes[file_hash] != file_name
            ):
                shutil.move(
                    destination_directory,
                    Path(dir_path) / source_files_hashes[file_hash],
                )

    for file_hash, file_name in source_files_hashes.items():
        if file_hash not in destination_files_hashes:
            shutil.copy(source_directory / file_name, destination_directory / file_name)


if __name__ == "__main__":
    src_path, dest_path = sys.argv[1:]

    sync(src_path, dest_path)
