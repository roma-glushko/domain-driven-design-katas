import hashlib
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Generator


def hash_file(file_path: Path, block_size: int = 65536) -> str:
    hasher = hashlib.sha1()

    with open(file_path, "rb") as file:
        block = file.read(block_size)
        while block:
            hasher.update(block)
            block = file.read(block_size)

        return hasher.hexdigest()


def get_directory_content(directory_path: str) -> Dict[str, str]:
    """
    Retrieve directory's files and their hashes by directory path
    :param directory_path: str
    :return: Dict[str, str]
    """
    directory_content: Dict[str, str] = {}

    for dir_path, _, file_names in os.walk(directory_path):
        for file_name in file_names:
            file_path: Path = Path(dir_path) / file_name
            directory_content[hash_file(file_path)] = file_name

    return directory_content


def plan_sync_actions(
    source_content: Dict[str, str],
    destination_content: Dict[str, str],
    source_path: str,
    destination_path: str,
) -> Generator:
    for hash, file_name in source_content.items():
        if hash not in destination_content:
            file_src_path = Path(source_path) / file_name
            file_dst_path = Path(destination_path) / file_name

            yield "copy", file_src_path, file_dst_path
            continue

        if (
            hash in destination_content
            and source_content[hash] != destination_content[hash]
        ):
            current_file_name = Path(destination_path) / destination_content[hash]
            new_file_name = Path(destination_path) / file_name

            yield "move", current_file_name, new_file_name
            continue

    for hash, file_name in destination_content.items():
        if hash in source_content:
            continue

        yield "delete", Path(destination_path) / file_name


def sync(source_path: str, destination_path: str):
    source_content = get_directory_content(source_path)
    destination_content = get_directory_content(destination_path)

    sync_actions = plan_sync_actions(
        source_content, destination_content, source_path, destination_path
    )

    for action, *file_paths in sync_actions:
        if action == "delete":
            os.remove(*file_paths)

        if action == "copy":
            shutil.copyfile(*file_paths)

        if action == "move":
            shutil.move(*file_paths)


if __name__ == "__main__":
    src_path, dest_path = sys.argv[1:]

    sync(src_path, dest_path)
