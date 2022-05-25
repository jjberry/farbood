import numpy as np
from parameters import Parameters
from midi import create_midi_file


class Path:
    # Data structure to store a path
    def __init__(self, pitches, log_prob, melody):
        self.path = pitches
        self.score = log_prob
        self.last_melody = melody


def generate_counterpoint(cf_pitches: list, param: Parameters) -> list:
    # first step: get candidates
    # assume we are above the c.f.
    start_pitch = cf_pitches[0]
    paths = []
    for interval, p in param.harmonic_table.items():
        if p > 0:
            paths.append(Path([start_pitch + param.interval2num[interval]], np.log(p), 'P1'))
            # print(start_pitch + interval2num[interval], np.log(p), 'P1')

    # next step: for each note in melodic_interval_names find the path in that results in max score
    for step in range(1, len(cf)):
        new_paths = []
        ref_pitch = cf_pitches[step]
        for interval, p in param.harmonic_table.items():
            if p > 0:
                cand_pitch = ref_pitch + param.interval2num[interval]
                # print("candidate: ", cand_pitch, interval)
                candidates = []
                scores = []
                for path in paths:
                    prev_pitch = path.path[-1]
                    melodic_interval = cand_pitch - prev_pitch
                    if melodic_interval not in param.melodic_num2interval:
                        continue
                    interval_name = param.melodic_num2interval[melodic_interval]
                    index = param.melodic_interval_inds[interval_name]
                    score = p * param.melodic_table[path.last_melody][index]

                    new_path = path.path.copy()
                    new_path.append(cand_pitch)
                    new_score = path.score + np.log(score)
                    candidates.append(Path(new_path, new_score, interval_name))
                    scores.append(new_score)
                    # print(new_path, new_score, interval_name)
                new_paths.append(candidates[np.argmax(scores)])
        paths = new_paths.copy()
    return paths


if __name__ == "__main__":
    p = Parameters()
    cf = ['D4', 'F4', 'G4', 'A4', 'G4', 'F4', 'E4', 'D4']
    print("cantus firmus: ")
    print(cf)
    cf_pitch = [p.note2pitch[n] for n in cf]
    counterpoints = generate_counterpoint(cf_pitch, p)
    print("generated paths: ")
    for path in counterpoints:
        print([p.pitch2note[n] for n in path.path], path.score)
    create_midi_file(cf_pitch, counterpoints[3].path, "test.midi")
