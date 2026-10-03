# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = math.pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << Measure(qubits[0], cbits[i])
    prog << Measure(qubits[0], cbits[measurements - 1])

    result = qvm.run_with_configuration(prog, cbits, shots)

    live_predictions = dud_predictions = detonations = 0

    if bomb_live:
        for key, value in result.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = result.get('0', 0)
        dud_predictions = result.get('1', 0)
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
