# EVAL_META: task_id=68, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, RY, Measure
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

    prog = qvm.qProg() if hasattr(qvm, 'qProg') else None
    from pyqpanda import QProg
    prog = QProg()

    for i in range(cycles):
        prog << RY(qubits[0], e)
        if bomb_live:
            prog << Measure(qubits[0], cbits[i])
    prog << Measure(qubits[0], cbits[measurements - 1])

    counts = qvm.run_with_configuration(prog, cbits, shots)

    def normalize_key(k):
        # ensure bitstring of length 'measurements', ordering cbit[0]..cbit[n-1]
        k = k.zfill(measurements)
        # QPanda returns keys with cbit[high]...cbit[low]; reverse to get cbit[0] first
        return k[::-1]

    if bomb_live:
        for key, value in counts.items():
            bits = normalize_key(key)
            # bits[measurements-1] corresponds to final measurement (Qiskit key[0])
            final_bit = bits[measurements - 1]
            intermediate = bits[:measurements - 1]
            if final_bit == '1':
                detonations += value
            elif '1' in intermediate:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        for key, value in counts.items():
            b = key.zfill(1)[-1]
            if b == '0':
                live_predictions += value
            else:
                dud_predictions += value
        detonations = 0

    qvm.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
