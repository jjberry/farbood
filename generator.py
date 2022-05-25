import numpy as np
from parameters import Parameters
from midi import create_midi_file


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


def generate_counterpoint(cf_pitches: list) -> list:
    param = Parameters()

    # Initialize: generate the trellis for all states based on the cantus
    trellis = []
    for t in range(len(cf_pitches)):
        notes = []
        for interval, p in param.harmonic_table.items():
            if p > 0:
                notes.append(Note(cf_pitches[t] + param.interval2num(interval), interval, np.log(p)))
                notes.append(Note(cf_pitches[t] - param.interval2num(interval), interval, np.log(p)))
        trellis.append(notes)

    # Viterbi algorithm: for each note in melodic_interval_names find the path in that results in max score
    paths = [Path([n], n.score, 'P1') for n in trellis[0]]
    for step in range(1, len(cf_pitches)):
        new_paths = []
        for n in trellis[step]:
            new_paths.extend(get_paths(n, paths, param))
        paths = new_paths.copy()

    return paths


def get_paths(cand_note: Note, prev_paths: list, param: Parameters) -> list:
    candidates = []
    scores = []
    outputs = []
    for path in prev_paths:
        prev_pitch = path.path[-1].pitch

        # Apply melodic rules
        score = np.exp(cand_note.score)
        score *= apply_melodic_table(cand_note.pitch, prev_pitch, path, param)
        if score == 0:  # eliminate divide by 0 warnings
            continue

        # TODO: Other rule evaluations go here

        # Create the new path for the next round
        new_path = path.path.copy()
        new_path.append(cand_note)
        new_score = path.score + np.log(score)
        candidates.append(Path(new_path, new_score, param.melodic_num2interval(cand_note.pitch - prev_pitch)))
        scores.append(new_score)

    # Get the best path for each state
    # Sometimes there are ties for best path. In that case add all ties
    best = np.max(scores)
    for c in range(len(candidates)):
        if scores[c] == best:
            outputs.append(candidates[c])
    return outputs


def apply_melodic_table(cand_pitch: int, prev_pitch: int, path: Path, param: Parameters) -> float:
    melodic_interval = cand_pitch - prev_pitch
    if not param.is_valid_melodic_interval(melodic_interval):
        return 0.0
    interval_name = param.melodic_num2interval(melodic_interval)
    return param.get_melodic_score(path.last_melody, interval_name)


def generate_cantus(n_steps: int, start_note: str) -> list:
    # Use the melody_table to draw samples
    params = Parameters()
    start_pitch = params.note2pitch(start_note)
    current_path = Path([start_pitch, np.log(1.0), 'P1'])

    return current_path.path


if __name__ == "__main__":
    p = Parameters()
    cf = ['D4', 'F4', 'G4', 'A4', 'G4', 'F4', 'E4', 'D4']
    print("cantus firmus: ")
    print(cf)
    cf_pitch = [p.note2pitch(n) for n in cf]
    counterpoints = generate_counterpoint(cf_pitch)
    print("generated paths: ")
    for path in counterpoints:
        print([p.pitch2note(n.pitch) for n in path.path], path.score)
    create_midi_file(cf_pitch, [n.pitch for n in counterpoints[3].path], "test.midi")
