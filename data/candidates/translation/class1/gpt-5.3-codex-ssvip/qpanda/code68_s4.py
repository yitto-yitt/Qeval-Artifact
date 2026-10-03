# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import *
import math

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
    shots = 1024
    cycles = 25
    e = math.pi / cycles

    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(cycles + 1 if bomb_live else 1)

    prog = QProg()
    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << Measure(q[0], c[i])
    prog << Measure(q[0], c[(cycles if bomb_live else 0)])

    result = machine.run_with_configuration(prog, c, shots)

    if bomb_live:
        for key, value in result.items():
            bits = key.replace(" ", "")
            if len(bits) < cycles + 1:
                bits = bits.zfill(cycles + 1)
            if bits[0] == '1':
                detonations += value
            elif '1' in bits[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = result.get('0', 0)
        dud_predictions = result.get('1', 0)
        detonations = 0

    machine.finalize()
    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
