# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
from numpy import pi


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = dud_predictions = detonations = 0
    shots = 1024
    cycles = 25
    e = pi / cycles

    qvm = pq.CPUQVM()
    qvm.init_qvm()

    qubits = qvm.qAlloc_many(1)

    if bomb_live:
        cbits = qvm.cAlloc_many(cycles + 2)
        prog = pq.QProg()
        for i in range(cycles):
            prog << pq.RY(qubits[0], e)
            prog << pq.Measure(qubits[0], cbits[i + 1])
        prog << pq.Measure(qubits[0], cbits[0])
        prog << pq.Measure(qubits[0], cbits[cycles + 1])

        counts = qvm.run_with_configuration(prog, cbits, shots)

        for key, value in counts.items():
            if key[0] == "1":
                detonations += value
            elif "1" in key[1:]:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        cbits = qvm.cAlloc_many(1)
        prog = pq.QProg()
        for _ in range(cycles):
            prog << pq.RY(qubits[0], e)
        prog << pq.Measure(qubits[0], cbits[0])

        counts = qvm.run_with_configuration(prog, cbits, shots)

        live_predictions = counts["0"] if "0" in counts else 0
        dud_predictions = counts["1"] if "1" in counts else 0
        detonations = 0

    qvm.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
