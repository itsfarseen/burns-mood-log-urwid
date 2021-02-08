from pathlib import Path
from mood_log import MoodLog


class Explorer:
    def __init__(self, rootdir):
        self._rootdir: Path = Path(rootdir)
        assert self._rootdir.is_dir()

    def list(self):
        for file in self._rootdir.iterdir():
            if file.name.endswith(".dml"):
                yield ExplorerEntry(file)


class ExplorerEntry:
    def __init__(self, path):
        self._path = path

    def name(self):
        return self._path.name

    def open(self):
        dml = MoodLog(filename=self._path, readonly=False)
        dml.load()
        dml.set_readonly(True)
        return dml
