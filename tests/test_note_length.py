import pytest
from hypothesis import given, assume
from hypothesis.strategies import sampled_from, decimals, floats, fractions, integers

from fractions import Fraction as Frac
import omk_core as omk

base_note_lengths = [omk.NoteLength(2,n) for n in [1,2,4,8,16,32,64,128,256]]
dotted_note_lengths = [nl.dot(d) for d in range(1, 10) for nl in base_note_lengths]
tupled_note_lengths = [omk.NoteLength.TupletMember(nl, tt) 
                        for tt in range(1, 100)
                        for nl in base_note_lengths]

dotted_tupled_note_lengths = [omk.NoteLength.TupletMember(nl, tt) 
                                for tt in range(1, 100)
                                for nl in dotted_note_lengths]

note_lengths = base_note_lengths + dotted_note_lengths + tupled_note_lengths + dotted_tupled_note_lengths
fractions = [Frac(nl) for nl in note_lengths]


@given(sampled_from(note_lengths), sampled_from(note_lengths))
def test_add_subtract_note_lengths(x, y):
    
    assert x + y - y == x
    assert y + x - x == y
    assert x - y + y == x
    assert y - x + x == y

@given(sampled_from(note_lengths), sampled_from(fractions))
def test_add_subtract_note_lengths_fractions(x, y):
    
    assert x + y - y == x
    assert y + x - x == y
    assert x - y + y == x
    assert y - x + x == y

    assert type(y + x) is type(x)
    assert type(y - x) is type(x)

@given(sampled_from(note_lengths), sampled_from(fractions))
def test_mul_note_lengths_fractions(x, y):

    assert x * y == y * x
    assert (x * y) / y == x

@given(sampled_from(base_note_lengths), integers(0,10))
def test_dots(nl, d):
    assert (nl, d) == nl.dot(d).undot()


@given(sampled_from(base_note_lengths), sampled_from([3,5,7,11,13]))
def test_undot_prime_tuples(x, y):

    assert not omk.NoteLength.TupletMember(x, y)._can_undot()

@given(sampled_from(dotted_note_lengths))
def test_undot(x):
    assert x._can_undot()

@given(sampled_from(base_note_lengths), integers(2,20))
def test_tuple_untuple(nl, tt):

    note_length, tuplet_type = omk.NoteLength.TupletMember(nl, tt).untuple()

    if omk.utils.math.is_pow2(tt):
        assert tuplet_type is None
    else:
        best_tt = omk.utils.math.divide_by_largest_pow2_factor(tt)

        assert note_length == nl
        assert best_tt == tuplet_type

@given(sampled_from(base_note_lengths), sampled_from([3,5,7,11,13]))
def test_tuple_repr(nl, tt):
    rpr = omk.NoteLength.TupletMember(nl, tt).__repr__()
    assert rpr == "NoteLength.TupletMember({}, {})".format(nl.__repr__(), tt.__repr__())

@given(sampled_from(base_note_lengths), integers(1,9))
def test_dotted_repr(nl, d):
    rpr = nl.dot(d).__repr__()
    assert rpr == "{}.dot({})".format(nl.__repr__(), str(d))