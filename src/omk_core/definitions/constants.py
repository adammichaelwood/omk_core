from dotmap import DotMap

D_LEN = 7  # "Diatonic Length" - The number of tones in a diatonic scale.
C_LEN = 12 # "Chromatic Length" - The number of tones in a chromatic scale.

# "M_ajor Scale"
MS = [
    # diatonic value, chromatic value, interval quality (0 or 0.5), letter name, solfege list, function, diszonance
    {'d':0, 'c':0,  'q':0,   'in': 'unison',  'ln':"c", 'sf':['do'],  'f': 'tonic',        'z': 0},
    {'d':1, 'c':2,  'q':0.5, 'in': 'second',  'ln':"d", 'sf':['re'],  'f': 'subtonic',     'z': 2},
    {'d':2, 'c':4,  'q':0.5, 'in': 'third',   'ln':"e", 'sf':['mi'],  'f': 'mediant',      'z': 1},
    {'d':3, 'c':5,  'q':0,   'in': 'fourth',  'ln':"f", 'sf':['fa'],  'f': 'subdominant',  'z': 2},
    {'d':4, 'c':7,  'q':0,   'in': 'fifth',   'ln':"g", 'sf':['sol'], 'f': 'dominant',     'z': 0},
    {'d':5, 'c':9,  'q':0.5, 'in': 'sixth',   'ln':"a", 'sf':['la'],  'f': 'submediant',   'z': 1},
    {'d':6, 'c':11, 'q':0.5, 'in': 'seventh', 'ln':"b", 'sf':['ti'],  'f': 'leading tone', 'z': 3}
]

MS = [DotMap(x) for x in MS]

# Accidentals
AC = {
    # halfsteps : verbose, unicode, ascii, ly
    -4 : {'v': 'quadruple flat', 'u':'𝄫𝄫', 'a':'bbbb', 'ly':'isisisis' },
    -3 : {'v': 'triple flat', 'u':'𝄫♭', 'a':'bbb', 'ly':'isisis'},
    -2 : {'v': 'double flat', 'u':'𝄫', 'a':'bb', 'ly':'isis' },
    -1 : {'v': 'flat', 'u':'♭', 'a':'b', 'ly':'is'},
     0 : {'v': 'natural', 'u':'♮', 'a':'', 'ly':''},
     1 : {'v': 'sharp', 'u':'♯', 'a':'#', 'ly':'es'},
     2 : {'v': 'double sharp', 'u':'𝄪', 'a':'##', 'ly':'eses'},
     3 : {'v': 'triple sharp', 'u':'𝄪♯', 'a':'###', 'ly':'eseses'},
     4 : {'v': 'quaduple sharp', 'u':'𝄪𝄪', 'a':'####', 'ly':'eseseses'},
}

AC = {i:DotMap(x) for i,x in AC.items()}

### I think everything below this line can be removed ###
#class Quality:
#    def __init__(self, label, inv="", abbr=""):
#
#        self.label = label
#        self.abbr = abbr or label[:3]
#
#    def __repr__(self):
#        return self.label


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
#    def __init__(self, diatonic_value, chromatic_value, name_in_c="", interval_quality="", interval_label=""):
#        self.diaonic_value = diatonic_value
#        self.chromatic_value = chromatic_value
#        self.name_in_c = name_in_c
#        self.interval_quality = interval_quality
#        self.interval_label = interval_label

#    def __repr__(self):
#        return f"ScaleDegree({{self.diatonic_value}}, {{self.chromatic_value}})"
