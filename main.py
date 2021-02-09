#!/bin/python
import urwid
import os
import sys
from explorer_widget import ExplorerWidget
from explorer import Explorer
from pathlib import Path
from crypto import Crypto, InvalidPassword
from getpass import getpass

if len(sys.argv) != 2: # argv[0] is main.py
    print("Usage: dml <directory>")
    sys.exit(-1)

dml_dir = Path(sys.argv[1])

if dml_dir.is_file():
    print("Given directory is actually a file.")
    sys.exit(-1)

if not dml_dir.exists():
    print("Directory does not exist.")
    sys.exit(-1)


def unhandled_input(key):
    if key in ["esc"]:
        raise urwid.ExitMainLoop()


palette = [
    ("selected", "yellow,bold", "default"),
    ("button-hover", "white,bold", "dark gray"),
    ("button-normal", "white", "dark gray"),
    ("bright", "default,bold", "default"),
    ("default", "default", "default"),
]

while True:
    password = getpass()
    crypto = Crypto(password)

    root = urwid.Padding(
        ExplorerWidget(
            Explorer(Path(dml_dir)),
        ),
        align="center",
        width=130,
    )

    loop = urwid.MainLoop(root, palette, unhandled_input=unhandled_input, pop_ups=True)
    try:
        loop.run()
    except InvalidPassword:
        print("Invalid password. \n")
        continue
    break
