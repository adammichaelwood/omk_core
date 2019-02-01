from dotmap import DotMap

D_LEN = 7  # "Diatonic Length" - The number of tones in a diatonic scale.
C_LEN = 12 # "Chromatic Length" - The number of tones in a chromatic scale.

NUMBERS = [
    # zero indx, music degree, interval name, ordinal name, ordinal suffix, roman numeral
    {'zi':0, 'md':1, 'i_name':'unison', 'ord':'first', 'ord_suf':'st', 'rn':'i'},
    {'zi':1, 'md':2, 'i_name':'second', 'ord':'second', 'ord_suf':'nd', 'rn':'ii'},
    {'zi':2, 'md':3, 'i_name':'third', 'ord':'third', 'ord_suf':'rd', 'rn':'iii'},
    {'zi':3, 'md':4, 'i_name':'fourth', 'ord':'fourth', 'ord_suf':'th', 'rn':'iv'},
    {'zi':4, 'md':5, 'i_name':'fifth', 'ord':'fifth', 'ord_suf':'th', 'rn':'v'},
    {'zi':5, 'md':6, 'i_name':'sixth', 'ord':'sixth', 'ord_suf':'th', 'rn':'vi'},
    {'zi':6, 'md':7, 'i_name':'seventh', 'ord':'seventh', 'ord_suf':'th', 'rn':'vii'},
    {'zi':7, 'md':8, 'i_name':'octave', 'ord':'eighth', 'ord_suf':'th', 'rn':'viii'},
    {'zi':8, 'md':9, 'i_name':'ninth', 'ord':'ninth', 'ord_suf':'th', 'rn':'ix'},
    {'zi':9, 'md':10, 'i_name':'tenth', 'ord':'tenth', 'ord_suf':'th', 'rn':'x'},
    {'zi':10, 'md':11, 'i_name':'eleventh', 'ord':'eleventh', 'ord_suf':'th', 'rn':'xi'},
    {'zi':11, 'md':12, 'i_name':'twelfth', 'ord':'twelfth', 'ord_suf':'th', 'rn':'xii'},
    {'zi':12, 'md':13, 'i_name':'thirteenth', 'ord':'thirteenth', 'ord_suf':'th', 'rn':'xiii'},
]

NUMBERS = [DotMap(item) for item in NUMBERS]



#class Quality:
#    def __init__(self, label, inv="", abbr=""):
#
#        self.label = label
#        self.abbr = abbr or label[:3]
#
#    def __repr__(self):
#        return self.label


# I don't think I'm using this anywhere now.
# cf. 
# to_PER, to_MAJ, to_MIN, to_AUG, to_DIM
#MAJOR = Quality("Major", "minor", (None, 0, -1, 1, -2))
#MINOR = Quality("minor", "Major", (None, 1, 0, 2, -1))
#PERFECT = Quality("Perfect", "Perfect", (0, None, None, 1, -1))
#AUGMENTED = Quality("Augmented", "diminished")
#DIMINISHED = Quality("diminished", "Augmented")
#DBL_AUGMENTED = Quality("Double Augmented", "double diminished", "DBL_AUG")
#DBL_DIMINISHED = Quality("double diminished", "Double Augmented", "dbl_dim")





#DIATONIC = [
#    (0, 0, "c", PERFECT, "unison"),    # 0
#    (1, 2, "d", MAJOR, "second"),      # 1
#    (2, 4, "e", MAJOR, "third"),       # 2
#    (3, 5, "f", PERFECT, "fourth"),    # 3
#    (4, 7, "g", PERFECT, "fifth"),     # 4
#    (5, 9, "a", MAJOR, "sixth"),       # 5
#    (6, 11, "b", PERFECT, "seventh")   # 6
#]

#class ScaleDegree:
#
#    def __init__(self, diatonic_value, chromatic_value, i_name_in_c="", interval_quality="", interval_label=""):
#        self.diaonic_value = diatonic_value
#        self.chromatic_value = chromatic_value
#        self.i_name_in_c = i_name_in_c
#        self.interval_quality = interval_quality
#        self.interval_label = interval_label
#
#    def __repr__(self):
#        return f"ScaleDegree({{self.diatonic_value}}, {{self.chromatic_value}})"
