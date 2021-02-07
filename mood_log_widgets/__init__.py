from mood_log_widgets.emotions_widget import EmotionsWidget
from mood_log_widgets.thoughts_widget import ThoughtsWidget
from mood_log import MoodLog

import urwid
import sys

class HeaderWidget(urwid.WidgetWrap):
    def __init__(self, dml: MoodLog):

        title = urwid.Text("Mood Log")
        title = urwid.AttrMap(title, "bright")

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

        w = urwid.Pile([("pack", title), ("pack", column)])
        super().__init__(w)

