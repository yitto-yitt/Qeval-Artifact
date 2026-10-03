# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    theta = np.pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    init(QMachineType.CPU)
    try:
        # Detect the bit order of run_with_configuration in pyqpanda.
        probe_q = qAlloc_many(2)
        probe_c = cAlloc_many(2)
        probe_prog = QProg()
        probe_prog << X(probe_q[0])
        probe_prog << Measure(probe_q[0], probe_c[0])
        probe_prog << Measure(probe_q[1], probe_c[1])
        probe_counts = run_with_configuration(probe_prog, probe_c, 4)
        probe_key = next(iter(probe_counts))
        vector_order = (probe_key[0] == '1')

        q = qAlloc_many(1)
        c = cAlloc_many(measurements)
        prog = QProg()
        for i in range(cycles):
            prog << RY(q[0], theta)
            if bomb_live:
                prog << Measure(q[0], c[i])
        prog << Measure(q[0], c[measurements - 1])

        counts = run_with_configuration(prog, c, shots)

        def get_bit(bitstring, idx):
            if vector_order:
                return bitstring[idx]
            return bitstring[measurements - 1 - idx]

        if bomb_live:
            final_idx = measurements - 1
            for key, value in counts.items():
                if get_bit(key, final_idx) == '1':
                    detonations += value
                elif any(get_bit(key, i) == '1' for i in range(final_idx)):
                    dud_predictions += value
                else:
                    live_predictions += value
        else:
            live_predictions = counts.get('0', 0)
            dud_predictions = counts.get('1', 0)
            detonations = 0
    finally:
        destroyQuantumMachine()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
