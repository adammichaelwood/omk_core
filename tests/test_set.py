import omk_core as omk

_MS = [
    (0, 0),
    (1, 2),
    (2, 4),
    (3, 5), 
    (4, 7), 
    (5, 9),
    (6,11)
]

tonal_tuples = [(x[0],(x[1]+m)%12) for m in [0,1,-1] for x in _MS]

tonal_vectors = [omk.TonalVector(x) for x in tonal_tuples]

tonal_oct_tuples = [(x[0], x[1], y) for y in [0,1,2,-1,-2] for x in tonal_tuples]

tonal_oct_vectors = [omk.TonalVector(x) for x in tonal_oct_tuples]