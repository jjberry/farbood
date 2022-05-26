from generator import *
from parameters import *

import numpy as np

p = Parameters()


def test_apply_melodic_table():
    note = Note(60, "P1", np.log(0.1))
    path = Path([note], np.log(0.1), "P1")
    cand_note = Note(63, "m3", np.log(0.1428))
    score = apply_melodic_table(cand_note, path, p)
    assert score == 0.08


def test_generate_cantus():
    n = Note(60, "P1", np.log(1.0))
    cantus = generate_cantus(8, n, p)
    assert len(cantus) == 8
