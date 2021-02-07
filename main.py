import urwid
import os

from bread_crumb import BreadCrumb
from button import Button
from mood_log import MoodLog, EMOTIONS, DISTORTIONS
from emotions_widgets import EmotionsWidget
from thoughts_widgets import ThoughtsWidget
from pprint import pprint


def exit_on_q(key):
    if key in ("q", "Q"):
        raise urwid.ExitMainLoop()


palette = [
    ("selected", "yellow,bold", "default"),
    ("button-hover", "white,bold", "dark gray"),
    ("button-normal", "white", "dark gray"),
    ("bright", "default,bold", "default"),
    ("bg", "white", "black"),
]

dml = MoodLog()
# if os.path.exists("test.json"):
#     dml.read("test.json")


def upsetting_event():
    edit = urwid.Edit(caption="Upsetting Event: ")
    # urwid.connect_signal(edit, "change", dml.on_update_upsetting_event())
    return urwid.LineBox(edit)

pile = urwid.Pile(
    [
        ("pack", upsetting_event()),
        ("pack", urwid.LineBox(EmotionsWidget(dml))),
        ("weight", 1, urwid.LineBox(ThoughtsWidget(dml))),
    ]
)
# render_thoughts()


root = urwid.Padding(pile, align="center", width=120)
loop = urwid.MainLoop(root, palette, unhandled_input=exit_on_q)
loop.run()
# dml.save("test.json")
