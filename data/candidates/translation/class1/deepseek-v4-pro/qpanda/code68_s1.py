# EVAL_META: task_id=68, framework=qpanda, class=1
from math import pi
import pyqpanda3.core as pq

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    if bomb_live:
        measurements = cycles + 1  # 26
    else:
        measurements = 1

    pq.init(pq.CPU)
    try:
        machine = pq.init_quantum_machine(pq.CPU)
        q = machine.qAlloc_many(1)
        c = machine.cAlloc_many(measurements)

        prog = pq.QProg()
        if bomb_live:
            for i in range(cycles):
                prog << pq.RY(q[0], e) << pq.Measure(q[0], c[i])
            # final measurement on last classical bit
            prog << pq.Measure(q[0], c[measurements - 1])
        else:
            for _ in range(cycles):
                prog << pq.RY(q[0], e)
            prog << pq.Measure(q[0], c[0])

        counts = pq.run_with_configuration(prog, c, shots)

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
    finally:
        pq.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
