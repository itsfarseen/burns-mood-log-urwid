import json

DISTORTIONS = {
    "SB": "Self Blame",
    "MF": "Mental Filter",
}

EMOTIONS = [
    ["Sad", "Blue", "Depressed", "Down", "Unhappy"],
    ["Anxious", "Worried", "Panicky", "Nervous", "Frightened"],
]


class Emotions:
    def __init__(self, variants):
        self._variants = variants
        self._selected = set()
        self._pct_before = 0
        self._pct_after = 0

    def variants(self):
        return self._variants

    def is_selected(self, variant):
        assert variant in self._variants
        return variant in self._selected

    def select(self, variant):
        assert variant in self._variants
        self._selected.add(variant)

    def unselect(self, variant):
        self._selected.remove(variant)

    def get_pct_before(self):
        return self._pct_before

    def set_pct_before(self, val):
        assert isinstance(val, int)
        self._pct_before = val

    def get_pct_after(self):
        return self._pct_after

    def set_pct_after(self, val):
        assert isinstance(val, int)
        self._pct_after = val


class Distortions:
    def __init__(self):
        self._selected = set()

    def get_label(self):
        return ", ".join(self._selected)

    def is_selected(self, value):
        return value in self._selected

    def select(self, value):
        assert value in DISTORTIONS
        self._selected.add(value)

    def unselect(self, value):
        self._selected.remove(value)


class Thought:
    def __init__(self):
        self._negative_thought = ""
        self._pct_before = 0
        self._pct_after = 0
        self._positive_thought = ""
        self._pct_belief = 0
        self._distortions = Distortions()

    def get_negative_thought(self):
        return self._negative_thought

    def set_negative_thought(self, val):
        self._negative_thought = val

    def get_pct_before(self):
        return self._pct_before

    def set_pct_before(self, val):
        assert isinstance(val, int)
        self._pct_before = val

    def get_pct_after(self):
        return self._pct_after

    def set_pct_after(self, val):
        assert isinstance(val, int)
        self._pct_after = val

    def get_positive_thought(self):
        return self._positive_thought

    def set_positive_thought(self, val):
        self._positive_thought = val

    def get_pct_belief(self):
        return self._pct_belief

    def set_pct_belief(self, val):
        assert isinstance(val, int)
        self._pct_belief = val

    def get_distortions(self):
        return self._distortions


class MoodLog:
    def __init__(self):
        self._upsetting_event = ""
        self._emotions = [Emotions(variants) for variants in EMOTIONS]
        self._thoughts = []

    def get_upsetting_event(self):
        return self._upsetting_event

    def set_upsetting_event(self, val):
        self._upsetting_event = val

    def get_emotions(self):
        return self._emotions

    def add_thought(self):
        thought = Thought()
        self._thoughts.append(thought)
        return thought

    def get_thoughts(self):
        return self._thoughts

    def delete_thought(self, idx):
        del self._thoughts[idx]

    # def save(self, filename):
    #     json.dump(self.data, open(filename, "w"))
    #
    # def read(self, filename):
    #     self.data = json.load(open(filename, "r"))
