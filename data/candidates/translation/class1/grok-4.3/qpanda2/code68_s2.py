# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
from numpy import pi
import builtins

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAllocMany(1)
    shots = 1024
    cycles = 25
    e = pi / cycles
    if bomb_live:
        n_cbits = cycles + 1
    else:
        n_cbits = 1
    c = machine.cAllocMany(n_cbits)
    prog = QProg()
    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])
    prog << Measure(q[0], c[n_cbits - 1])
    counts = machine.run_with_configuration(prog, shots)
    live_predictions = dud_predictions = detonations = 0
    if bomb_live:
        for key, value in counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts['0'] if '0' in counts else 0
        dud_predictions = counts['1'] if '1' in counts else 0
        detonations = 0
    total = shots
    return {
        "live_predictions": live_predictions / total,
        "dud_predictions": dud_predictions / total,
        "detonations": detonations / total,
    }
