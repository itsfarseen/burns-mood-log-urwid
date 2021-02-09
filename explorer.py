from pathlib import Path
from mood_log import MoodLog
from diary import Diary
from datetime import datetime


class Explorer:
    def __init__(self, rootdir):
        self._rootdir: Path = Path(rootdir)
        assert self._rootdir.is_dir()

    def list(self):
        for file in reversed(sorted(self._rootdir.iterdir())):
            if file.name.endswith(".dml"):
                yield ExplorerEntry(file, type="dml")
            elif file.name.endswith(".diary"):
                yield ExplorerEntry(file, type="diary")

    def new_diary(self):
        date = datetime.now()
        filename = date.strftime("%Y-%m-%d--%H-%M.diary")
        path = self._rootdir/filename
        return ExplorerEntry(path, type="diary")

    def new_dml(self):
        date = datetime.now()
        filename = date.strftime("%Y-%m-%d--%H-%M.dml")
        path = self._rootdir/filename
        return ExplorerEntry(path, type="dml")


class ExplorerEntry:
    def __init__(self, path, type):
        self._path = path
        self._type = type

    def name(self):
        return self._path.name

    def open(self):
        if self._type == "dml":
            dml = MoodLog(filename=self._path, readonly=False)
        elif self._type == "diary":
            dml = Diary(filename=self._path, readonly=False)
        else:
            raise ValueError("Unexpected type: " + self._type)
        if self._path.exists():
            dml.load()
        else:
            dml.mark_dirty()
        dml.set_readonly(True)
        return dml

    def get_type(self):
        return self._type
