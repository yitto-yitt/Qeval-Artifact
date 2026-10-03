# EVAL_META: task_id=68, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, QProg, RY
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles

    qvm = CPUQVM()
    qvm.init_qvm()

    measurements = cycles + 1 if bomb_live else 1
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(measurements)

    prog = QProg()
    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << qvm.get_qmachine_type  # placeholder removed below

    # Rebuild program properly using measurement operations
    prog = QProg()
    from pyqpanda import Measure
    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << Measure(qubits[0], cbits[i])
    prog << Measure(qubits[0], cbits[measurements - 1])

    counts = qvm.run_with_configuration(prog, cbits, shots)

    qvm.finalize()

    normalized = {}
    for key, value in counts.items():
        k = key.replace(' ', '')
        if len(k) < measurements:
            k = k.zfill(measurements)
        normalized[k] = normalized.get(k, 0) + value

    if bomb_live:
        for key, value in normalized.items():
            if key[0] == '1':
                detonations += value
            elif '1' in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        live_predictions = normalized.get('0', 0)
        dud_predictions = normalized.get('1', 0)
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
