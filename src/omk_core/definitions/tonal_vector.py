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

class TonalVector():

    def __init__(self, t):

        self.d = t[0]
        self.c = t[1]
        self._Q = MS[self.d] # Q for source # rename?

    ### As a chroma (note) ###

    # letter name
    @property
    def _ln(self):
        return self._Q['ln']

    # how sharp or flat
    @property
    def _modifier(self): 
        return self.d - self._Q['d']



    ### As an interval ###
    