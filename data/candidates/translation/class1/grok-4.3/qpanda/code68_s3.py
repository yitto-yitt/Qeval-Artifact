# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import *
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi/cycles
    measurements = cycles + 1 if bomb_live else 1
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(1)
    c_bits = qvm.cAlloc_many(measurements)
    prog = QProg()
    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << Measure(qubits[0], c_bits[i+1])
    prog << Measure(qubits[0], c_bits[0])
    result = qvm.run_with_configuration(prog, c_bits, shots)
    counts = result
    if bomb_live:
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0', 0)
        dud_predictions = counts.get('1', 0)
        detonations = 0
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
