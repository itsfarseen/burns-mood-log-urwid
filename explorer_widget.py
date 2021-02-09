import urwid
from button import Button
from mood_log_widgets import MoodLogWidget
from diary_widget import DiaryWidget
from datetime import datetime
from mood_log import MoodLog
from diary import Diary


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
            urwid.connect_signal(
                btn, "click", lambda _b, entry=entry: self._open(entry)
            )
            entry_widgets.append(btn)
            entry_widgets.append(urwid.Divider("."))

        add_btn = Button("New Mood Log")
        urwid.connect_signal(
            add_btn, "click", lambda _btn: self._new_mood_log()
        )
        entry_widgets.append(add_btn)

        add_btn = Button("New Diary Entry")
        urwid.connect_signal(add_btn, "click", lambda _btn: self._new_diary())
        entry_widgets.append(add_btn)

        entries_list = urwid.ListBox(urwid.SimpleFocusListWalker(entry_widgets))
        entries_list = urwid.LineBox(entries_list)

        title = urwid.Text("Mood Log Explorer", align="center")
        title = urwid.AttrMap(title, "bright")
        title = urwid.Filler(title, top=1)
        w = urwid.Pile(
            [
                (2, title),
                ("weight", 1, entries_list),
                ("pack", urwid.Text("Esc: Exit")),
            ]
        )
        self._w.original_widget = w

    def _new_mood_log(self):
        entry = self._explorer.new_dml()
        self._open(entry)

    def _new_diary(self):
        entry = self._explorer.new_diary()
        self._open(entry)

    def _open(self, entry):
        if entry.get_type() == "dml":
            dmlw = MoodLogWidget(entry.open())
        elif entry.get_type() == "diary":
            dmlw = DiaryWidget(entry.open())
        else:
            raise ValueError("Unexpected type: " + entry.get_type())
        urwid.connect_signal(dmlw, "close", lambda _w: self._render())
        self._w.original_widget = dmlw
