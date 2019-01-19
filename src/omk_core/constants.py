D_LEN = 7  # "Diatonic Length" - The number of tones in a diatonic scale.
C_LEN = 12 # "Chromatic Length" - The number of tones in a chromatic scale.

class Quality:
    def __init__(self, label, inv="", abbr=""):

        self.label = label
        self.abbr = abbr or label[:3]

    def __repr__(self):
        return self.label


# to_PER, to_MAJ, to_MIN, to_AUG, to_DIM
MAJOR = Quality("Major", "minor", (None, 0, -1, 1, -2))
MINOR = Quality("minor", "Major", (None, 1, 0, 2, -1))
PERFECT = Quality("Perfect", "Perfect", (0, None, None, 1, -1))
AUGMENTED = Quality("Augmented", "diminished")
DIMINISHED = Quality("diminished", "Augmented")
DBL_AUGMENTED = Quality("Double Augmented", "double diminished", "DBL_AUG")
DBL_DIMINISHED = Quality("double diminished", "Double Augmented", "dbl_dim")





DIATONIC = [
    (0, 0, "c", PERFECT, "unison"),    # 0
    (1, 2, "d", MAJOR, "second"),      # 1
    (2, 4, "e", MAJOR, "third"),       # 2
    (3, 5, "f", PERFECT, "fourth"),    # 3
    (4, 7, "g", PERFECT, "fifth"),     # 4
    (5, 9, "a", MAJOR, "sixth"),       # 5
    (6, 11, "b", PERFECT, "seventh")   # 6
]

class ScaleDegree:

    def __init__(self, diatonic_value, chromatic_value, name_in_c="", interval_quality="", interval_label=""):
        self.diaonic_value = diatonic_value
        self.chromatic_value = chromatic_value
        self.name_in_c = name_in_c
        self.interval_quality = interval_quality
        self.interval_label = interval_label

    def __repr__(self):
        return f"ScaleDegree({{self.diatonic_value}}, {{self.chromatic_value}})"
