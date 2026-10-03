# EVAL_META: task_id=68, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import CPUQVM, QProg, RY
try:
    from pyqpanda3.core import measure
except ImportError:
    from pyqpanda3.core import Measure as measure

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles

    measurements = cycles + 1 if bomb_live else 1

    machine = CPUQVM()
    machine.init_qvm()

    qubit = machine.qAlloc()
    cbits = machine.cAlloc_many(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(qubit, e)
        if bomb_live:
            prog << measure(qubit, cbits[i])
    prog << measure(qubit, cbits[-1])

    counts = machine.run_with_configuration(prog, cbits, shots)
    machine.finalize_qvm()

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
