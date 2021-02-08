import urwid
import os

from bread_crumb import BreadCrumb
from button import Button
from explorer_widget import ExplorerWidget
from explorer import Explorer
from pathlib import Path


def exit_on_q(key):
    if key in ["esc"]:
        raise urwid.ExitMainLoop()


palette = [
    ("selected", "yellow,bold", "default"),
    ("button-hover", "white,bold", "dark gray"),
    ("button-normal", "white", "dark gray"),
    ("bright", "default,bold", "default"),
    ("default", "default", "default"),
]

root = urwid.Padding(ExplorerWidget(Explorer(Path("."))), align="center", width=120)
loop = urwid.MainLoop(root, palette, unhandled_input=exit_on_q, pop_ups=True)
loop.run()
# dml.save("test.json")
