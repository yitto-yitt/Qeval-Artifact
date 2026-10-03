# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
from math import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    live_predictions = 0
    dud_predictions = 0
    detonations = 0
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
            prog.insert(pq.RY(qubits[0], e))
            prog.insert(pq.Measure(qubits[0], cbits[i + 1]))

        prog.insert(pq.Measure(qubits[0], cbits[0]))
        prog.insert(pq.Measure(qubits[0], cbits[cycles + 1]))

        readout_cbits = [cbits[0]] + [cbits[i] for i in range(cycles, 0, -1)] + [cbits[cycles + 1]]
        counts = qvm.run_with_configuration(prog, readout_cbits, shots)

        for raw_key, value in counts.items():
            key = str(raw_key)
            final_is_one = (len(key) > 0 and (key[0] == "1" or key[-1] == "1"))
            middle = key[1:-1] if len(key) > 2 else ""
            if final_is_one:
                detonations += value
            elif "1" in middle:
                dud_predictions += value
            else:
                live_predictions += value
    else:
        cbits = qvm.cAlloc_many(2)
        prog = pq.QProg()

        for _ in range(cycles):
            prog.insert(pq.RY(qubits[0], e))

        prog.insert(pq.Measure(qubits[0], cbits[0]))
        prog.insert(pq.Measure(qubits[0], cbits[1]))

        counts = qvm.run_with_configuration(prog, cbits, shots)

        for raw_key, value in counts.items():
            key = str(raw_key)
            if "1" in key:
                dud_predictions += value
            else:
                live_predictions += value

        detonations = 0

    qvm.finalize()

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
