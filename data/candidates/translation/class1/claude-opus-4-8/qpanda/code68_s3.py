# EVAL_META: task_id=68, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, RY, measure
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = CPUQVM()
    qvm.allocate_qubits(1)
    qvm.allocate_cbits(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(0, e)
        if bomb_live:
            prog << measure(0, i)
    prog << measure(0, measurements - 1)

    qvm.run(prog, shots)
    counts = qvm.result().get_counts()

    def normalize(k):
        k = k.replace(" ", "")
        if len(k) < measurements:
            k = k.zfill(measurements)
        return k[::-1]

    norm_counts = {}
    for key, value in counts.items():
        nk = normalize(key)
        norm_counts[nk] = norm_counts.get(nk, 0) + value

    if bomb_live:
        for key, value in norm_counts.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = norm_counts.get('0', 0)
        dud_predictions = norm_counts.get('1', 0)
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
