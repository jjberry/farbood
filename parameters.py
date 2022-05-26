import numpy as np

class Note:
    # Data structure to store note information
    def __init__(self, pitch: int, harmonic_interval: str, log_prob: float):
        self.pitch = pitch                          # the midi pitch number
        self.harmonic_interval = harmonic_interval  # the interval to the cantus note
        self.score = log_prob                       # this is from the harmonic table


class Path:
    # Data structure to store a path
    def __init__(self, notes: list, log_prob: float, melody: str):
        self.path = notes           # the list of Note objects in the path
        self.score = log_prob       # the score of the path
        self.last_melody = melody   # the interval between path[-1] and path[-2]


class Parameters:

    def __init__(self):
        note_names = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
        midi_num = 12  # C0
        midi2note = {}
        note2midi = {}
        for octave in range(9):
            for note in note_names:
                key = note + str(octave)
                midi2note[midi_num] = key
                note2midi[key] = midi_num
                midi_num += 1

        interval_names = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'd5', 'P5', 'm6', 'M6', 'm7', 'M7', 'P8',
                          'm9', 'M9', 'm10', 'M10']
        interval2num = {}
        num2interval = {}
        for num, interval in enumerate(interval_names):
            interval2num[interval] = num
            num2interval[num] = interval

        # harmonic table is defined in the paper
        harmonic_table = {'P1': 0.0, 'm2': 0.0, 'M2': 0.0, 'm3': 0.1428, 'M3': 0.1428, 'P4': 0.0, 'd5': 0.0,
                          'P5': 0.1428, 'm6': 0.1428, 'M6': 0.1428, 'm7': 0.0, 'M7': 0.0, 'P8': 0.0004, 'm9': 0.0,
                          'M9': 0.0, 'm10': 0.1428, 'M10': 0.1428}

        melodic_interval_names = ['m2u', 'M2u', 'm3u', 'M3u', 'P4u', 'P5u', 'm6u', 'P8u',
                                  'm2d', 'M2d', 'm3d', 'M3d', 'P4d', 'P5d', 'P8d', 'P1']
        melodic_interval_inds = {n: i for i, n in enumerate(melodic_interval_names)}
        melodic_interval2num = {}
        melodic_num2interval = {}
        for k, v in zip(melodic_interval_names, [1, 2, 3, 4, 5, 7, 8, 12, -1, -2, -3, -4, -5, -7, -12, 0]):
            melodic_interval2num[k] = v
            melodic_num2interval[v] = k

        # melodic table is defined in the paper
        melodic_table = {
            'm2u': [0.0, 0.45, 0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.035, 0.035, 0.025, 0.025, 0.01, 0.01, 0.009, 0.001],
            'M2u': [0.45, 0.45, 0.03, 0.03, 0.0, 0.0, 0.0, 0.0, 0.01, 0.01, 0.005, 0.005, 0.004, 0.004, 0.002, 0.001],
            'm3u': [0.45, 0.45, 0.03, 0.03, 0.0, 0.0, 0.0, 0.0, 0.01, 0.01, 0.005, 0.005, 0.004, 0.004, 0.002, 0.001],
            'M3u': [0.35, 0.35, 0.05, 0.05, 0.0, 0.0, 0.0, 0.0, 0.05, 0.05, 0.025, 0.025, 0.025, 0.025, 0.024, 0.001],
            'P4u': [0.065, 0.065, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.4, 0.02, 0.02, 0.01, 0.01, 0.009, 0.001],
            'P5u': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.52, 0.52, 0.01, 0.01, 0.01, 0.01, 0.009, 0.001],
            'm6u': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.51, 0.51, 0.025, 0.025, 0.01, 0.01, 0.009, 0.001],
            'P8u': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.51, 0.51, 0.025, 0.025, 0.01, 0.01, 0.009, 0.001],
            'm2d': [0.05, 0.05, 0.005, 0.005, 0.002, 0.002, 0.002, 0.002, 0.0, 0.467, 0.2, 0.2, 0.015, 0.0, 0.0, 0.001],
            'M2d': [0.05, 0.05, 0.005, 0.005, 0.002, 0.002, 0.002, 0.002, 0.367, 0.367, 0.1, 0.1, 0.015, 0.0, 0.0,
                    0.001],
            'm3d': [0.366, 0.366, 0.005, 0.005, 0.002, 0.002, 0.002, 0.002, 0.05, 0.05, 0.1, 0.1, 0.0, 0.0, 0.0, 0.001],
            'M3d': [0.366, 0.366, 0.005, 0.005, 0.002, 0.002, 0.002, 0.002, 0.05, 0.05, 0.1, 0.1, 0.0, 0.0, 0.0, 0.001],
            'P4d': [0.43, 0.43, 0.02, 0.02, 0.02, 0.02, 0.039, 0.02, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001],
            'P5d': [0.454, 0.454, 0.03, 0.03, 0.01, 0.005, 0.005, 0.011, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001],
            'P8d': [0.454, 0.454, 0.03, 0.03, 0.01, 0.005, 0.005, 0.011, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001],
            'P1': [0.1, 0.1, 0.08, 0.08, 0.05, 0.05, 0.04, 0.03, 0.1, 0.1, 0.08, 0.08, 0.05, 0.04, 0.02, 0.0]
        }
        for k in melodic_interval_names:  # normalize because some rows don't sum to 1
            melodic_table[k] = list(np.array(melodic_table[k]) / sum(melodic_table[k]))

        ##############
        # Parameters #
        ##############
        # Map Note names to Midi pitch number starting at C0 = 12
        self.note_names = note_names
        self.pitch2note_map = midi2note
        self.note2pitch_map = note2midi

        # Map vertical interval names (the interval between the cantus firmus and the counterpoint at time t)
        # Goes from root (P1) to Major 10th (M10)
        self.interval_names = interval_names
        self.interval2num_map = interval2num
        self.num2interval_map = num2interval
        # Probabilities of vertical intervals
        self.harmonic_table = harmonic_table

        # Map horizontal interval names (how the melody changes from time t-1 to time t)
        # Limited to specific intervals up or down, e.g. minor 2nd up (m2u) or Perfect 5th down (P5d)
        self.melodic_interval_names = melodic_interval_names
        self.melodic_interval_inds = melodic_interval_inds  # used to index the melodic table
        self.melodic_interval2num_map = melodic_interval2num
        self.melodic_num2interval_map = melodic_num2interval
        # Conditional probabilities of melody moving from state t-1 to state t
        self.melodic_table = melodic_table

    # Helper functions
    def note2pitch(self, note: str) -> int:
        return self.note2pitch_map[note]

    def pitch2note(self, pitch: int) -> str:
        return self.pitch2note_map[pitch]

    def interval2num(self, interval: str) -> int:
        return self.interval2num_map[interval]

    def num2interval(self, num: int) -> str:
        return self.num2interval_map[num]

    def melodic_interval2num(self, interval: str) -> int:
        return self.melodic_interval2num_map[interval]

    def melodic_num2interval(self, num: int) -> str:
        return self.melodic_num2interval_map[num]

    def get_melodic_score(self, last_interval: str, current_interval: str) -> float:
        index = self.melodic_interval_inds[current_interval]
        return self.melodic_table[last_interval][index]

    def is_valid_melodic_interval(self, interval: int) -> bool:
        return interval in self.melodic_num2interval_map

    def get_melodic_interval(self, note: Note, path: Path):
        num = note.pitch - path.path[-1].pitch
        return self.melodic_num2interval(num)


