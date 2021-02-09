import urwid


class BreadCrumb(urwid.Widget):
    _sizing = frozenset(["flow", "fixed"])

    __selected = False
    signals = ["change", "postchange"]

    def __init__(self, label, selected=False, readonly=False):
        self._label = label
        self.__selected = selected
        self._readonly = readonly

    def rows(self, size, focus=False):
        return 1

    def pack(self, size, focus=False):
        return (len(self._label), 1)

    def render(self, size, focus=False):
        text = self._label
        if size[0] < len(text):
            text = text[: size[0]]
        elif size[0] > len(text):
            pad = " " * (size[0] - len(text))
            text = text + pad

        cursor = (0, 0) if focus else None
        attr = [[("selected", len(text))]] if self.__selected else None
        return urwid.TextCanvas(text=[text.encode()], cursor=cursor, attr=attr)

    def get_cursor_coords(self, size):
        return (0, 0)

    def keypress(self, size, key):
        if not self._readonly and self._command_map[key] == "activate":
            new_selected = not self.__selected
            self._emit("change", new_selected)
            self.__selected = new_selected
            self._invalidate()
            return None

        return key

    def selectable(self):
        return not self._readonly
