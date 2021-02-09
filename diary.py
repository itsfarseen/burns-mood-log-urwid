from read_only_guard import ReadOnlyGuard
from pathlib import Path
from crypto import Crypto
from datetime import datetime
import shutil


class Diary:
    def __init__(self, filename, readonly):
        self._filename = filename
        self._readonly_guard = ReadOnlyGuard(readonly=readonly)
        self._contents = ""

    def save(self):
        path = Path(self._filename)
        if path.exists():
            tempdir = path.parent / ".dmlbackups"
            if not tempdir.exists():
                tempdir.mkdir()

            now = datetime.now()
            nowstr = now.strftime("%Y-%m-%d--%H-%M")
            bakfilename = path.name + "-" + nowstr + ".bak"
            bakfile = tempdir / bakfilename
            shutil.copyfile(path, bakfile)

        contents = self._contents
        Crypto.instance.write_file(path, contents)

        self._readonly_guard.clear_dirty()

    def is_readonly(self):
        return self._readonly_guard.is_readonly()

    def set_readonly(self, val):
        return self._readonly_guard.set_readonly(val)

    def is_dirty(self):
        return self._readonly_guard.is_dirty()

    def mark_dirty(self):
        self._readonly_guard._dirty = True

    def get_contents(self):
        return self._contents

    def set_contents(self, val):
        self._readonly_guard.assert_not_readonly()

        self._contents = val

    def get_filename(self):
        return Path(self._filename).name

    def load(self):
        path = Path(self._filename)
        contents = Crypto.instance.read_file(path)
        self._contents = contents

        self._readonly_guard.clear_dirty()
