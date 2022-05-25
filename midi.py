import pretty_midi


def create_midi_file(cantus: list, counterpoint: list, filename: str):
    pm = pretty_midi.PrettyMIDI(initial_tempo=120)
    velocity = 100
    inst = pretty_midi.Instrument(program=0, is_drum=False)

    duration = 0.5  # quarter note at 120 bpm
    t = 0
    for i in range(len(cantus)):
        cf_note = pretty_midi.Note(velocity=velocity, pitch=cantus[i], start=t, end=t+duration)
        gn_note = pretty_midi.Note(velocity=velocity, pitch=counterpoint[i], start=t, end=t+duration)
        inst.notes.append(cf_note)
        inst.notes.append(gn_note)
        t += duration
    pm.instruments.append(inst)
    pm.write(filename)
