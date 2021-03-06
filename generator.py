import numpy as np
from parameters import Parameters, Note, Path
from midi import create_midi_file


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
        # Apply rules
        score = np.exp(cand_note.score)
        score *= apply_melodic_table(cand_note, path, param)

        # TODO: Other rule evaluations go here

        if score == 0:  # eliminate divide by 0 warnings
            continue
        # Create the new path for the next round
        new_path = path.path.copy()
        new_path.append(cand_note)
        new_score = path.score + np.log(score)
        candidates.append(Path(new_path, new_score, param.get_melodic_interval(cand_note, path)))
        scores.append(new_score)

    # Get the best path for each state
    # Sometimes there are ties for best path. In that case add all ties
    best = np.max(scores)
    for c in range(len(candidates)):
        if scores[c] == best:
            outputs.append(candidates[c])
    return outputs


def apply_melodic_table(cand_note: Note, path: Path, param: Parameters) -> float:
    try:
        interval_name = param.get_melodic_interval(cand_note, path)
        return param.get_melodic_score(path.last_melody, interval_name)
    except KeyError:
        return 0.0


def generate_cantus(n_steps: int, start_note: Note, params: Parameters) -> list:
    # Use the melody_table to draw samples using np.random.choice()
    path = Path([start_note], np.log(1.0), 'P1')
    for step in range(n_steps - 1):
        draw = np.random.choice(params.melodic_interval_names, p=params.melodic_table[path.last_melody])
        draw_pitch = params.melodic_interval2num(draw)
        pitch = path.path[-1].pitch + draw_pitch
        note = Note(pitch, "", np.log(1.0))
        new_path = path.path.copy()
        new_path.append(note)
        path = Path(new_path, np.log(1.0), draw)

    return path.path


if __name__ == "__main__":
    p = Parameters()
    start_note = Note(60, "P1", 0.0)
    cf = generate_cantus(8, start_note, p)
    print("cantus firmus: ")
    print([p.pitch2note(n.pitch) for n in cf])
    cf_pitch = [n.pitch for n in cf]
    counterpoints = generate_counterpoint(cf_pitch)
    print("generated paths: ")
    for path in counterpoints:
        print([p.pitch2note(n.pitch) for n in path.path], path.score)
    create_midi_file(cf_pitch, [n.pitch for n in counterpoints[3].path], "test.midi")
