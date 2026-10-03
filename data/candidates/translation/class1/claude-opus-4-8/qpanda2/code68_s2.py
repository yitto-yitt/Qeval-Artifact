# EVAL_META: task_id=68, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, QProg, RY, measure, pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(q[0], e)
        if bomb_live:
            prog << measure(q[0], c[i])
    prog << measure(q[0], c[measurements - 1])

    raw_counts = qvm.run_with_configuration(prog, c, shots)

    # Normalize keys to fixed-width bit strings ordered so index 0 is the last measurement
    counts = {}
    for key, value in raw_counts.items():
        norm_key = key.zfill(measurements)
        counts[norm_key] = counts.get(norm_key, 0) + value

    if bomb_live:
        for key, value in counts.items():
            # key: bit at position 0 corresponds to classical bit index (measurements-1)
            # QPanda returns MSB-first for highest classical index.
            # Qiskit's key[0] is the last measurement (index measurements-1),
            # which corresponds to the leftmost (MSB) bit here.
            last_bit = key[0]
            earlier_bits = key[1:]
            if last_bit == '1':
                detonations += value
            elif '1' in earlier_bits:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = counts.get('0', 0)
        dud_predictions = counts.get('1', 0)
        detonations = 0

    qvm.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
