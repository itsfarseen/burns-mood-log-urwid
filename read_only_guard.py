class ReadOnlyGuard:
    def __init__(self, readonly=True):
        self._readonly = readonly
        self._dirty = False

    def is_readonly(self):
        return self._readonly

    def set_readonly(self, val):
        assert isinstance(val, bool)
        self._readonly = val

    def assert_not_readonly(self):
        assert not self._readonly
        self._dirty = True

    def is_dirty(self):
        return self._dirty

    def clear_dirty(self):
        self._dirty = False
