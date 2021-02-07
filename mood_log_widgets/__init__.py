from mood_log_widgets.emotions_widget import EmotionsWidget
from mood_log_widgets.thoughts_widget import ThoughtsWidget
from mood_log import MoodLog

import urwid
import sys

shortcuts = {"save": "ctrl o", "back": "ctrl x"}


class MoodLogWidget(urwid.WidgetWrap):
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
        if self._dml.is_readonly():
            if key == shortcuts["back"]:
                self._dml.set_readonly(False)
                self._render()
                return None
        else:
            if not self._dml.is_dirty():
                if key == shortcuts["back"]:
                    self._dml.set_readonly(True)
                    self._render()
                    return None

            if key == shortcuts["save"]:
                self._dml.save()
                return None

        retval = super().keypress(size, key)
        self._footer.update_status()
        return retval


class HeaderWidget(urwid.WidgetWrap):
    def __init__(self, dml: MoodLog):
        title = urwid.Text("Mood Log", align="center")
        title = urwid.AttrMap(title, "bright")
        title = urwid.Filler(title, top=1)

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
        self._status = urwid.Text("")

        if dml.is_readonly():
            shortcuts = urwid.Text("Ctrl-X: Edit")
        else:
            shortcuts = urwid.Text("Ctrl-O: Save  Ctrl-X: Go back")

        w = urwid.Columns([("weight", 1, shortcuts), ("pack", self._status)])
        super().__init__(w)

        self.update_status()

    def update_status(self):
        if self._dml.is_readonly():
            status_text = "Read-only mode"
        elif self._dml.is_dirty():
            status_text = "Unsaved changes."
        else:
            status_text = "Saved."

        self._status.set_text(status_text)
