import attr

from ..tonal_algebra.tonal_vector import TonalVector
from ..tonal_algebra.pitch import Pitch
from ..tonal_algebra.interval import Interval

from ..rhythm.note_length import NoteLength
from ..rhythm.time_signature import TimeSignature

@attr.s
class Note():
    """A note, having a definite pitch (or definite lack of one) and a definite rhythm (or definite lack of one),
    along with other attributes such as lyrics, expressions, chords, etc.)
    """

    pitch = attr.ib(type=Pitch)
    length = attr.ib(type=NoteLength)
    attributes = attr.ib(type=dict, default=dict())

    def __getattr__(self, attribute):
        print("0")
        return getattr(self.pitch, attribute)
        try:
            return self.attributes(attribute)
        except:
            print("1")

        try:
            return getattr(self.length, attribute)()
        except:
            print("2")

        try:
            return getattr(self.pitch, attribute)()
        except:
            print("3")

        print("4")
        return None