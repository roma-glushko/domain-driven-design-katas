import shutil
import tempfile
from pathlib import Path

from src.sync_dirs.main import sync


def test__sync__file_exists_in_src_dir_only():
    source = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()

    try:
        content = "Roman Glushko"
        (Path(source) / 'me.txt').write_text(content)
        sync(source, dest)
        expected_path = Path(dest) / 'me.txt'
        assert expected_path.exists()
        assert expected_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test__sync__file_exists_in_both_dirs_but_named_differently():
    source = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()

    try:
        content = "I am a file that was renamed"
        source_path = Path(source) / 'source-filename'
        old_dest_path = Path(dest) / 'dest-filename'
        expected_dest_path = Path(dest) / 'source-filename'
        source_path.write_text(content)
        old_dest_path.write_text(content)
        sync(source, dest)
        assert old_dest_path.exists() is False
        assert expected_dest_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test__sync__file_exists_in_dst_dir_only():
    source = tempfile.mkdtemp()
    dest = tempfile.mkdtemp()

    try:
        content = "I am a file that was renamed"
        dest_path = Path(dest) / 'file.txt'
        dest_path.write_text(content)

        sync(source, dest)

        assert dest_path.exists() is False
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
