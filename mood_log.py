import json
import datetime
from pathlib import Path
import pathlib
import shutil
import json
from crypto import Crypto

DISTORTIONS = {
    "AON": "All-or-Nothing Thinking",
    "OG": "Overgeneralization",
    "MF": "Mental Filter",
    "DP": "Discounting the Positive",
    "MR": "Mind Reading",
    "FT": "Fortune Telling",
    "MAG": "Magnification",
    "MIN": "Minimization",
    "SH": "Should Statements",
    "LAB": "Labelling",
    "SB": "Self Blame",
    "OB": "Other Blame",
}

# Note: List instead of set because we need to keep the order when showing in UI
EMOTIONS = [
    ["Sad", "Blue", "Depressed", "Down", "Unhappy"],
    ["Anxious", "Worried", "Panicky", "Nervous", "Frightened"],
]


class ReadOnlyGuard:
    def __init__(self, readonly=True):
        self._readonly = readonly
        self._dirty = False

    def is_readonly(self):
        return self._readonly

    def set_readonly(self, val):
        assert isinstance(val, bool)
        self._readonly = val

    def assert_not_readonly(self):
        assert not self._readonly
        self._dirty = True

    def is_dirty(self):
        return self._dirty

    def clear_dirty(self):
        self._dirty = False


class Emotions:
    def __init__(self, variants, readonly_guard):
        self._readonly_guard = readonly_guard
        self._variants = variants
        self._selected = set()
        self._pct_before = 0
        self._pct_after = 0

    def is_readonly(self):
        return self._readonly_guard.is_readonly()

    def variants(self):
        return self._variants

    def is_selected(self, variant):
        assert variant in self._variants
        return variant in self._selected

    def select(self, variant):
        self._readonly_guard.assert_not_readonly()

        assert variant in self._variants
        self._selected.add(variant)

    def unselect(self, variant):
        self._readonly_guard.assert_not_readonly()

        self._selected.remove(variant)

    def get_pct_before(self):
        return self._pct_before

    def set_pct_before(self, val):
        self._readonly_guard.assert_not_readonly()

        assert isinstance(val, int)
        self._pct_before = val

    def get_pct_after(self):
        return self._pct_after

    def set_pct_after(self, val):
        self._readonly_guard.assert_not_readonly()

        assert isinstance(val, int)
        self._pct_after = val

    def todict(self):
        return {
            "variants": list(self._variants),
            "selected": list(self._selected),
            "pct_before": self._pct_before,
            "pct_after": self._pct_after,
        }

    def fromdict(self, obj):
        self._readonly_guard.assert_not_readonly()

        self._variants = list(obj["variants"])
        self._selected = set(obj["selected"])
        self.set_pct_before(obj["pct_before"])
        self.set_pct_after(obj["pct_after"])


class Distortions:
    def __init__(self, readonly_guard):
        self._readonly_guard = readonly_guard
        self._selected = []

    def get_label(self):
        return ", ".join(self._selected)

    def is_selected(self, value):
        return value in self._selected

    def select(self, value):
        self._readonly_guard.assert_not_readonly()

        assert value in DISTORTIONS
        self._selected.append(value)
        self._resort()

    def unselect(self, value):
        self._readonly_guard.assert_not_readonly()

        self._selected.remove(value)
        self._resort()

    def _resort(self):
        self._readonly_guard.assert_not_readonly()

        keys = list(DISTORTIONS.keys())
        self._selected.sort(key=lambda k: keys.index(k))

    def todict(self):
        return {"selected": self._selected}

    def fromdict(self, obj):
        self._readonly_guard.assert_not_readonly()

        self._selected = obj["selected"]


class Thought:
    def __init__(self, readonly_guard):
        self._readonly_guard = readonly_guard
        self._negative_thought = ""
        self._pct_before = 0
        self._pct_after = 0
        self._positive_thought = ""
        self._pct_belief = 0
        self._distortions = Distortions(readonly_guard)

    def is_readonly(self):
        return self._readonly_guard.is_readonly()

    def get_negative_thought(self):
        return self._negative_thought

    def set_negative_thought(self, val):
        self._readonly_guard.assert_not_readonly()

        self._negative_thought = val

    def get_pct_before(self):
        return self._pct_before

    def set_pct_before(self, val):
        self._readonly_guard.assert_not_readonly()

        assert isinstance(val, int)
        self._pct_before = val

    def get_pct_after(self):
        return self._pct_after

    def set_pct_after(self, val):
        self._readonly_guard.assert_not_readonly()

        assert isinstance(val, int)
        self._pct_after = val

    def get_positive_thought(self):
        return self._positive_thought

    def set_positive_thought(self, val):
        self._readonly_guard.assert_not_readonly()

        self._positive_thought = val

    def get_pct_belief(self):
        return self._pct_belief

    def set_pct_belief(self, val):
        self._readonly_guard.assert_not_readonly()

        assert isinstance(val, int)
        self._pct_belief = val

    def get_distortions(self):
        return self._distortions

    def todict(self):
        return {
            "negative_thought": self._negative_thought,
            "pct_before": self._pct_before,
            "pct_after": self._pct_after,
            "positive_thought": self._positive_thought,
            "pct_belief": self._pct_belief,
            "distortions": self._distortions.todict(),
        }

    def fromdict(self, obj):
        self._readonly_guard.assert_not_readonly()

        self.set_negative_thought(obj["negative_thought"])
        self.set_pct_before(obj["pct_before"])
        self.set_pct_after(obj["pct_after"])
        self.set_positive_thought(obj["positive_thought"])
        self.set_pct_belief(obj["pct_belief"])
        self._distortions.fromdict(obj["distortions"])


class MoodLog:
    def __init__(self, filename, readonly=True, date=None):
        self._readonly_guard = ReadOnlyGuard(readonly)
        self._date = date or datetime.datetime.now()
        self._filename = filename
        self._upsetting_event = ""
        self._emotions = [
            Emotions(variants, self._readonly_guard) for variants in EMOTIONS
        ]
        self._thoughts = []

    def is_dirty(self):
        return self._readonly_guard.is_dirty()

    def is_readonly(self):
        return self._readonly_guard.is_readonly()

    def set_readonly(self, val):
        return self._readonly_guard.set_readonly(val)

    def get_date(self):
        return self._date

    def get_upsetting_event(self):
        return self._upsetting_event

    def set_upsetting_event(self, val):
        self._readonly_guard.assert_not_readonly()

        self._upsetting_event = val

    def get_emotions(self):
        return self._emotions

    def add_thought(self):
        self._readonly_guard.assert_not_readonly()

        thought = Thought(self._readonly_guard)
        self._thoughts.append(thought)
        return thought

    def get_thoughts(self):
        return self._thoughts

    def delete_thought(self, idx):
        self._readonly_guard.assert_not_readonly()

        del self._thoughts[idx]

    def todict(self):
        return {
            "date": self._date.strftime("%Y/%m/%d %H:%M"),
            "upsetting_event": self._upsetting_event,
            "emotions": [emotion.todict() for emotion in self._emotions],
            "thoughts": [thought.todict() for thought in self._thoughts],
        }

    def fromdict(self, obj):
        self._readonly_guard.assert_not_readonly()

        self._date = datetime.datetime.strptime(obj["date"], "%Y/%m/%d %H:%M")
        self.set_upsetting_event(obj["upsetting_event"])
        self._emotions = []
        for emdict in obj["emotions"]:
            em = Emotions(variants=None, readonly_guard=self._readonly_guard)
            em.fromdict(emdict)
            self._emotions.append(em)

        self._thoughts = []
        for thdict in obj["thoughts"]:
            th = Thought(self._readonly_guard)
            th.fromdict(thdict)
            self._thoughts.append(th)

    def fileexists(self):
        path = Path(self._filename)
        return path.exists()

    def save(self):
        path = Path(self._filename)
        if path.exists():
            tempdir = Path(".") / ".dmlbackups"
            if not tempdir.exists():
                tempdir.mkdir()

            now = datetime.datetime.now()
            nowstr = now.strftime("%Y-%m-%d--%H-%M")
            bakfilename = path.name + "-" + nowstr + ".bak"
            bakfile = tempdir / bakfilename
            shutil.copyfile(path, bakfile)

        obj = self.todict()
        contents = json.dumps(obj)
        Crypto.instance.write_file(path, contents)

        self._readonly_guard.clear_dirty()

    def load(self):
        path = Path(self._filename)
        contents = Crypto.instance.read_file(path)
        obj = json.loads(contents)
        self.fromdict(obj)

        self._readonly_guard.clear_dirty()
