import urwid
from button import Button
from mood_log_widgets import MoodLogWidget


class ExplorerWidget(urwid.WidgetWrap):
    def __init__(self, explorer):
        self._explorer = explorer
        super().__init__(urwid.WidgetPlaceholder(urwid.Text("")))
        self._render()

    def _render(self):
        entries = list(self._explorer.list())

        entry_widgets = []
        for entry in entries:
            btn = Button(entry.name(), normal_attr="default")
            urwid.connect_signal(btn, "click", lambda _b: self._open(entry))
            entry_widgets.append(btn)
            entry_widgets.append(urwid.Divider("."))
        entries_list = urwid.ListBox(urwid.SimpleFocusListWalker(entry_widgets))
        entries_list = urwid.LineBox(entries_list)

        w = urwid.Pile(
            [
                (
                    "pack",
                    urwid.AttrMap(urwid.Text("Mood Log Explorer"), "bright"),
                ),
                ("weight", 1, entries_list),
            ]
        )
        self._w.original_widget = w

    def _open(self, entry):
        dmlw = MoodLogWidget(entry.open())
        urwid.connect_signal(dmlw, "close", lambda _w: self._render())
        self._w.original_widget = dmlw
