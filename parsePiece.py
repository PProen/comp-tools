import music21 as m21
import random as rn


a = input("Type the filename here: ")

piece = m21.converter.parse(a)

dur_groups = []
for measure in piece.parts[0][1:]:
    measure_durs = []
    for nota in measure:
        value = float(nota.quarterLength)
        if value != 0.0:
            measure_durs.append(value)
    dur_groups.append(measure_durs)

possible_sums = []
for group in dur_groups:
    soma = round(sum(group),1)
    if soma not in possible_sums:
        possible_sums.append(soma)

dur_dict = dict()
for value in possible_sums:
    value_list = []
    for group in dur_groups:
        if round(sum(group),1) == value:
            value_list.append(group)
            
    dur_dict[value] = value_list

def create_dur_string(beats):
    possible_durs = possible_sums
    result = []
    beat = 0
    while beat < beats:
        new_beat = rn.choice(possible_durs)
        chosen_group = rn.choice(dur_dict[new_beat])
        result.append(chosen_group)
        beat += new_beat
    if beat > beats:
        diff = round(beat - beats, 1)
        for group in result:
            if group in dur_dict[diff]:
                result.remove(group)
                beat -= diff
                break
        if beat > beats:
            while beat > beats:
                ran_group = rn.choice(result)
                size = round(sum(ran_group),1)
                result.remove(ran_group)
                beat -= size
    if beat < beats:
        diff = beats - beat
        new_group = rn.choice(dur_dict[diff])
        result.append(new_group)
        beat += diff

    new_result = []
    for group in result:
        for nota in group:
            new_result.append(nota)
    return new_result

def create_pitch_string(scale, dur_string, rest_prob):
    result = []
    count = 0
    while count < len(dur_string):
        dur = dur_string[count]
        m = rn.random()
        if m < rest_prob:
            nota = m21.note.Rest()
        else:
            nota = m21.note.Note()
            nota.pitch.midi = rn.choice(scale)
        nota.quarterLength = dur
        result.append(nota)
        count += 1
    return result
