import urwid
from diary import Diary

shortcuts = {
    "save": "ctrl o",
    "toggle-edit": "ctrl x",
    "back": "esc",
    "discard": "ctrl r",
}


class DiaryWidget(urwid.WidgetWrap):
    signals = ["close"]

    def __init__(self, diary: Diary):
        self._diary = diary

        w = urwid.WidgetPlaceholder(urwid.Text(""))
        super().__init__(w)

        self._render()

    def _render(self):
        if self._diary.is_readonly():
            content = urwid.Text(self._diary.get_contents())
        else:
            content = urwid.Edit(
                edit_text=self._diary.get_contents(),
                multiline=True,
                allow_tab=True,
            )
            urwid.connect_signal(
                content, "change", lambda _w, val: self._diary.set_contents(val)
            )
        content = urwid.Filler(content, valign='top')

        self._body = urwid.Pile(
            [
                ("pack", HeaderWidget(self._diary)),
                ("weight", 1, urwid.LineBox(content)),
            ]
        )
        self._footer = FooterWidget(self._diary)
        frame = urwid.Frame(body=self._body, footer=self._footer)
        self._w.original_widget = frame

    def keypress(self, size, key):
        if key == shortcuts["toggle-edit"]:
            if self._diary.is_readonly():
                self._diary.set_readonly(False)
            else:
                self._diary.set_readonly(True)
            self._render()
        elif key == shortcuts["back"]:
            if not self._diary.is_dirty():
                self._emit("close")
        elif key == shortcuts["discard"]:
            self._emit("close")
        elif key == shortcuts["save"]:
            if self._diary.is_dirty():
                self._diary.save()
                self._footer.update_status()
        else:
            retval = super().keypress(size, key)
            self._footer.update_status()
            return retval

        return None


class HeaderWidget(urwid.WidgetWrap):
    def __init__(self, diary: Diary):
        title = urwid.Text("Diary", align="center")
        title = urwid.AttrMap(title, "bright")
        title = urwid.Filler(title, top=1)

        date = urwid.Text(diary.get_filename())

        column = urwid.Columns([("weight", 1, date)])
        column = urwid.LineBox(column)

        w = urwid.Pile([(2, title), ("pack", column)])
        super().__init__(w)


class FooterWidget(urwid.WidgetWrap):
    def __init__(self, diary: Diary):
        self._diary = diary

        super().__init__(urwid.WidgetPlaceholder(urwid.Text("")))

        self.update_status()

    def update_status(self):
        dml = self._diary

        status = urwid.Text("")

        ws = []
        ws.append(("pack", urwid.Text("Ctrl-O: Save")))
        if not dml.is_dirty():
            ws.append(("pack", urwid.Text("Esc: Go Back")))
        else:
            ws.append(("pack", urwid.Text("Ctrl-R: Discard and Go Back")))
        if dml.is_readonly():
            ws.append(("pack", urwid.Text("Ctrl-X: Edit mode")))
        else:
            ws.append(("pack", urwid.Text("Ctrl-X: Read-only mode")))

        ws.append(("weight", 1, urwid.Text("")))
        ws.append(("pack", status))

        status_text = ""
        if dml.is_readonly():
            status_text += "Read-only mode. "

        if dml.is_dirty():
            status_text += "Unsaved changes."
        else:
            status_text += "Saved."

        status.set_text(status_text)

        self._w.original_widget = urwid.Columns(ws, dividechars=3)
