import urwid
from mood_log import Emotions
from bread_crumb import BreadCrumb


class EmotionsWidget(urwid.WidgetWrap):
    def __init__(self, dml):
        w = urwid.Pile(
            [("pack", EmotionsHeader())]
            + [("pack", EmotionsRow(emotion)) for emotion in dml.get_emotions()]
        )
        super().__init__(w)


class EmotionsHeader(urwid.WidgetWrap):
    def __init__(self):
        header = urwid.Columns(
            [
                ("weight", 6, urwid.Text("Emotions")),
                ("weight", 1, urwid.Text("% Before")),
                ("weight", 1, urwid.Text("% After")),
            ],
        )
        header = urwid.AttrMap(header, "bright")
        divider = urwid.Divider("-")
        w = urwid.Pile(
            [
                ("pack", header),
                ("pack", divider),
            ]
        )
        super().__init__(w)


class EmotionsRow(urwid.WidgetWrap):
    def __init__(self, emotions: Emotions):
        self._emotions: Emotions = emotions

        btns = []
        for emotion in self._emotions.variants():
            btn = BreadCrumb(
                emotion,
                selected=self._emotions.is_selected(emotion),
                readonly=self._emotions.is_readonly(),
            )
            urwid.connect_signal(
                btn, "change", self._toggle_emotion_cb(emotion)
            )
            btns.append((14, btn))

        btns_box = urwid.Columns(btns, dividechars=1)

        if self._emotions.is_readonly():
            pct_before = urwid.Text(str(self._emotions.get_pct_before()))
            pct_after = urwid.Text(str(self._emotions.get_pct_after()))
        else:
            pct_before = urwid.IntEdit(default=self._emotions.get_pct_before())
            urwid.connect_signal(
                pct_before, "change", self._update_pct_before_cb()
            )

            pct_after = urwid.IntEdit(default=self._emotions.get_pct_after())
            urwid.connect_signal(
                pct_after, "change", self._update_pct_after_cb()
            )

        w = urwid.Columns(
            [
                ("weight", 6, btns_box),
                ("weight", 1, pct_before),
                ("weight", 1, pct_after),
            ]
        )
        super().__init__(w)

    def _toggle_emotion_cb(self, emotion):
        def fn(_widget, val):
            assert isinstance(val, bool)
            if val:
                self._emotions.select(emotion)
            else:
                self._emotions.unselect(emotion)

        return fn

    def _update_pct_before_cb(self):
        def fn(_widget, val):
            if val == "":
                val = "0"
            self._emotions.set_pct_before(int(val))

        return fn

    def _update_pct_after_cb(self):
        def fn(_widget, val):
            if val == "":
                val = "0"
            self._emotions.set_pct_after(int(val))

        return fn
