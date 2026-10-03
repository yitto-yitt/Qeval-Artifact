# EVAL_META: task_id=68, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, RY
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(measurements)

    prog = qvm.create_empty_qprog() if hasattr(qvm, "create_empty_qprog") else None
    from pyqpanda import QProg, measure
    prog = QProg()
    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << measure(qubits[0], cbits[i])
    prog << measure(qubits[0], cbits[measurements - 1])

    counts = qvm.run_with_configuration(prog, cbits, shots)

    def normalize_key(k):
        # QPanda returns keys where index 0 is the highest-order classical bit.
        # Reverse so that key[i] corresponds to cbit i (matching Qiskit's ordering
        # where the last measurement is the most significant / detonation bit).
        return k[::-1]

    if bomb_live:
        for key, value in counts.items():
            k = normalize_key(key)
            if k[-1] == '1':
                detonations += value
            elif '1' in k[:-1]:
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
