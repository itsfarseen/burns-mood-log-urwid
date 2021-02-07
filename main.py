import urwid
import os

from bread_crumb import BreadCrumb
from button import Button
from mood_log import MoodLog, EMOTIONS, DISTORTIONS
from mood_log_widgets import MoodLogWidget
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

dml = MoodLog(readonly=False)
# if os.path.exists("test.json"):
#     dml.read("test.json")

for i in range(20):
    dml.add_thought()
    dml.get_thoughts()[-1].set_positive_thought("Testing " + str(i))

dml._readonly_guard._dirty = False
# dml.set_readonly(True)


root = urwid.Padding(MoodLogWidget(dml), align="center", width=120)
loop = urwid.MainLoop(root, palette, unhandled_input=exit_on_q, pop_ups=True)
loop.run()
# dml.save("test.json")
