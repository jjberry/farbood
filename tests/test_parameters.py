from parameters import *


p = Parameters()


def test_note2pitch():
    assert p.note2pitch("C4") == 60


def test_pitch2note():
    assert p.pitch2note(60) == "C4"


def test_interval2num():
    assert p.interval2num("P5") == 7


def test_num2interval():
    assert p.num2interval(7) == "P5"


def test_melodic_interval2num():
    assert p.melodic_interval2num("P8d") == -12


def test_melodic_num2interval():
    assert p.melodic_num2interval(-7) == "P5d"


def test_get_melodic_score():
    assert p.get_melodic_score("P5d", "M3u") == 0.03


def test_is_valid_melodic_interval():
    assert not p.is_valid_melodic_interval(9)
    assert p.is_valid_melodic_interval(-7)

