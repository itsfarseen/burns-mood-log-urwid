from mood_log_widgets.emotions_widget import EmotionsWidget
from mood_log_widgets.thoughts_widget import ThoughtsWidget
from mood_log import MoodLog

import urwid
import sys

shortcuts = {
    "save": "ctrl o",
    "toggle-edit": "ctrl x",
    "back": "esc",
    "discard": "ctrl r",
}


class MoodLogWidget(urwid.WidgetWrap):
    signals = ["close"]

    def __init__(self, dml: MoodLog):
        self._dml = dml

        w = urwid.WidgetPlaceholder(urwid.Text(""))
        super().__init__(w)

        self._render()

    def _render(self):
        self._body = urwid.Pile(
            [
                ("pack", HeaderWidget(self._dml)),
                ("pack", urwid.LineBox(EmotionsWidget(self._dml))),
                ("weight", 1, urwid.LineBox(ThoughtsWidget(self._dml))),
            ]
        )
        self._footer = FooterWidget(self._dml)
        frame = urwid.Frame(body=self._body, footer=self._footer)
        self._w.original_widget = frame

    def keypress(self, size, key):
        if key == shortcuts["toggle-edit"]:
            if self._dml.is_readonly():
                self._dml.set_readonly(False)
            else:
                self._dml.set_readonly(True)
            self._render()
        elif key == shortcuts["back"]:
            if not self._dml.is_dirty():
                self._emit("close")
        elif key == shortcuts["discard"]:
            self._emit("close")
        elif key == shortcuts["save"]:
            if self._dml.is_dirty():
                self._dml.save()
                self._footer.update_status()
        else:
            retval = super().keypress(size, key)
            self._footer.update_status()
            return retval

        return None


class HeaderWidget(urwid.WidgetWrap):
    def __init__(self, dml: MoodLog):
        title = urwid.Text("Mood Log", align="center")
        title = urwid.AttrMap(title, "bright")
        title = urwid.Filler(title, top=1)

        if dml.is_readonly():
            upsetting_event = urwid.Text(
                "Upsetting event: " + dml.get_upsetting_event()
            )
        else:
            upsetting_event = urwid.Edit(
                caption="Upsetting event: ", edit_text=dml.get_upsetting_event()
            )
            urwid.connect_signal(
                upsetting_event,
                "change",
                lambda _w, val: dml.set_upsetting_event(val),
            )

        date = urwid.Text(dml.get_date().strftime("%d/%m/%y %H:%M"))

        column = urwid.Columns([("weight", 1, upsetting_event), ("pack", date)])
        column = urwid.LineBox(column)

        w = urwid.Pile([(2, title), ("pack", column)])
        super().__init__(w)


class FooterWidget(urwid.WidgetWrap):
    def __init__(self, dml: MoodLog):
        self._dml = dml

        super().__init__(urwid.WidgetPlaceholder(urwid.Text("")))

        self.update_status()

    def update_status(self):
        dml = self._dml

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
        if self._dml.is_readonly():
            status_text += "Read-only mode. "

        if self._dml.is_dirty():
            status_text += "Unsaved changes."
        else:
            status_text += "Saved."

        status.set_text(status_text)

        self._w.original_widget = urwid.Columns(ws, dividechars=3)
