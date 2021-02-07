import urwid
from mood_log import Thought, DISTORTIONS, Distortions
from button import Button
from bread_crumb import BreadCrumb


class ThoughtsWidget(urwid.WidgetWrap):
    def __init__(self, dml):
        self._dml = dml
        header = ThoughtsHeader()
        rows = []
        for idx, thought in enumerate(dml.get_thoughts()):
            row = self._create_thought_row(thought, idx)
            rows.append(row)

        add_btn = Button("Add Thought")
        urwid.connect_signal(add_btn, "click", self._add_thought_cb())
        add_btn = urwid.Padding(add_btn, align="left", width=15)
        rows.append(add_btn)

        rows_list = urwid.ListBox(urwid.SimpleFocusListWalker(rows))
        self._rows_list = rows_list

        w = urwid.Pile(
            [
                ("pack", header),
                ("weight", 1, rows_list),
            ]
        )
        super().__init__(w)

    def _create_thought_row(self, thought, idx):
        row = ThoughtsRow(thought)
        urwid.connect_signal(row, "delete", self._del_thought_cb(idx))
        return row

    def _add_thought_cb(self):
        def fn(_widget):
            thought = self._dml.add_thought()
            idx = len(self._dml.get_thoughts()) - 1
            row = self._create_thought_row(thought, idx)

            list_body = self._rows_list.body
            list_body.insert(-1, row)
            idx = len(list_body) - 2
            list_body.set_focus(idx)

        return fn

    def _del_thought_cb(self, idx):
        def fn(_widget):
            self._dml.delete_thought(idx)
            del self._rows_list.body[idx]

        return fn


class ThoughtsHeader(urwid.WidgetWrap):
    def __init__(self):
        header = urwid.Columns(
            [
                ("weight", 6, urwid.Text("Negative thought")),
                ("weight", 1, urwid.Text("% Bef.")),
                ("weight", 1, urwid.Text("% Aft.")),
                ("weight", 3, urwid.Text("Distortions")),
                ("weight", 6, urwid.Text("Positive thought")),
                ("weight", 1, urwid.Text("% Belf.")),
                (5, urwid.Text("")),
            ],
            dividechars=3,
        )
        header = urwid.AttrMap(header, "bright")
        divider = urwid.Divider("-")
        w = urwid.Pile([("pack", header), ("pack", divider)])
        super().__init__(w)


class ThoughtsRow(urwid.WidgetWrap):
    signals = ["delete"]

    def __init__(self, thought: Thought):
        self._thought: Thought = thought
        ws = []

        negative_thought = urwid.Edit(
            edit_text=thought.get_negative_thought(), multiline=True
        )
        urwid.connect_signal(
            negative_thought, "change", self._update_negative_thought_cb()
        )
        ws.append(("weight", 6, negative_thought))

        pct_before = urwid.IntEdit(default=thought.get_pct_before())
        urwid.connect_signal(pct_before, "change", self._update_pct_before_cb())
        ws.append(("weight", 1, pct_before))

        pct_after = urwid.IntEdit(default=thought.get_pct_after())
        urwid.connect_signal(pct_after, "change", self._update_pct_after_cb())
        ws.append(("weight", 1, pct_after))

        distortions = DistortionsPopupLauncher(self._thought.get_distortions())
        ws.append(("weight", 3, distortions))

        positive_thought = urwid.Edit(
            edit_text=thought.get_positive_thought(), multiline=True
        )
        urwid.connect_signal(
            positive_thought, "change", self._update_positive_thought_cb()
        )
        ws.append(("weight", 6, positive_thought))

        pct_belief = urwid.IntEdit(default=thought.get_pct_belief())
        urwid.connect_signal(pct_belief, "change", self._update_pct_belief_cb())
        ws.append(("weight", 1, pct_belief))

        del_btn = Button("Del")
        urwid.connect_signal(
            del_btn, "click", lambda _btn: self._emit("delete")
        )
        ws.append((5, del_btn))

        row = urwid.Columns(ws, dividechars=3)
        divider = urwid.Divider(".")
        w = urwid.Pile([("pack", row), ("pack", divider)])
        super().__init__(w)

    def _update_negative_thought_cb(self):
        def fn(_widget, val):
            self._thought.set_negative_thought(val)

        return fn

    def _update_pct_before_cb(self):
        def fn(_widget, val):
            if val == "":
                val = "0"
            self._thought.set_pct_before(int(val))

        return fn

    def _update_pct_after_cb(self):
        def fn(_widget, val):
            if val == "":
                val = "0"
            self._thought.set_pct_after(int(val))

        return fn

    def _update_positive_thought_cb(self):
        def fn(_widget, val):
            self._thought.set_positive_thought(val)

        return fn

    def _update_pct_belief_cb(self):
        def fn(_widget, val):
            if val == "":
                val = "0"
            self._thought.set_pct_belief(int(val))

        return fn


class DistortionsPopup(urwid.WidgetWrap):
    signals = ["close"]

    def __init__(self, distortions: Distortions):
        self._distortions = distortions

        items = []

        header = urwid.Text("Select Distortions")
        header = urwid.AttrMap(header, "bright")
        items.append(header)

        distortion_keys = DISTORTIONS.keys()
        for key in distortion_keys:
            btn = BreadCrumb(
                key + ": " + DISTORTIONS[key],
                selected=distortions.is_selected(key),
            )
            urwid.connect_signal(btn, "change", self._update_distortion_cb(key))
            items.append(btn)

        btn = Button("OK")
        urwid.connect_signal(btn, "click", lambda _btn: self._emit("close"))
        items.append(btn)

        w = urwid.Pile(items)
        w = urwid.Filler(urwid.LineBox(w))
        super().__init__(w)

    def _update_distortion_cb(self, distortion):
        def fn(_widget, selected):
            if selected:
                self._distortions.select(distortion)
            else:
                self._distortions.unselect(distortion)

        return fn


class DistortionsPopupLauncher(urwid.PopUpLauncher):
    def __init__(self, distortions: Distortions):
        self._distortions = distortions

        w = urwid.Button(distortions.get_label())
        urwid.connect_signal(w, "click", lambda _btn: self.open_pop_up())
        super().__init__(w)

    def create_pop_up(self):
        popup = DistortionsPopup(self._distortions)
        urwid.connect_signal(popup, "close", self._popup_close_cb())
        return popup

    def _popup_close_cb(self):
        def fn(_widget):
            self.close_pop_up()
            self.original_widget.set_label(self._distortions.get_label())

        return fn

    def get_pop_up_parameters(self):
        return {"left": 0, "top": 1, "overlay_width": 32, "overlay_height": 7}
