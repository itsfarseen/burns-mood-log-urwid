import json
import datetime

DISTORTIONS = {
    "SB": "Self Blame",
    "MF": "Mental Filter",
}

EMOTIONS = [
    ["Sad", "Blue", "Depressed", "Down", "Unhappy"],
    ["Anxious", "Worried", "Panicky", "Nervous", "Frightened"],
]


class ReadOnlyGuard:
    def __init__(self, readonly=True):
        self._readonly = readonly

    def is_readonly(self):
        return self._readonly

    def set_readonly(self, val):
        assert isinstance(val, bool)
        self._readonly = val

    def assert_not_readonly(self):
        assert not self._readonly


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


class MoodLog:
    def __init__(self, readonly=True):
        self._readonly_guard = ReadOnlyGuard(readonly)
        self._date = datetime.datetime.now()
        self._upsetting_event = ""
        self._emotions = [
            Emotions(variants, self._readonly_guard) for variants in EMOTIONS
        ]
        self._thoughts = []

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

    # def save(self, filename):
    #     json.dump(self.data, open(filename, "w"))
    #
    # def read(self, filename):
    #     self.data = json.load(open(filename, "r"))
