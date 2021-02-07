import urwid


class Button(urwid.Widget):
    _sizing = frozenset(["flow", "fixed", "box"])
    _selectable = True

    signals = ["click"]

    def __init__(
        self,
        label,
        hover_attr="button-hover",
        normal_attr="button-normal",
        label_prefix=" ",
        label_suffix=" ",
    ):
        self._label = label_prefix + label + label_suffix
        self.hover_attr = hover_attr
        self.normal_attr = normal_attr

    def rows(self, size, focus=False):
        return 1

    def pack(self, size, focus=False):
        return (len(self._label), 1)

    def render(self, size, focus=False):
        text = self._label
        if len(size) >= 1:
            if size[0] < len(text):
                text = text[: size[0]]
            elif size[0] > len(text):
                pad = " " * (size[0] - len(text))
                text = text + pad
        cursor = (1, 0) if focus else None
        attr = [[(self.hover_attr if focus else self.normal_attr, len(text))]]
        return urwid.TextCanvas(text=[text.encode()], cursor=cursor, attr=attr)

    def get_cursor_coords(self, size):
        return (1, 0)

    def keypress(self, size, key):
        if self._command_map[key] == "activate":
            self._emit("click")
            return None
        return key
