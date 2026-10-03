# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi
import numpy as np

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    dev = qml.device("default.qubit", wires=1, shots=shots)

    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            samples = []
            for i in range(cycles):
                qml.RY(e, wires=0)
                samples.append(qml.sample(qml.PauliZ(0)))
            return qml.sample(qml.PauliZ(0))
        # We need per-cycle measurements; implement with mid-circuit measurements

    live_predictions = dud_predictions = detonations = 0

    if bomb_live:
        @qml.qnode(dev)
        def circuit():
            outcomes = []
            for i in range(cycles):
                qml.RY(e, wires=0)
                m = qml.measure(0)
                outcomes.append(m)
            return [qml.sample(m) for m in outcomes]

        results = circuit()
        results = np.array(results)  # shape (cycles, shots)
        for s in range(shots):
            col = results[:, s]
            # first cycle measurement is index 0, last is index cycles-1
            # In qiskit: measurements = cycles+1, key[0] is last measured bit (final),
            # but final measure duplicates last cycle measurement
            # key ordering: qiskit bit string reversed; key[0]=c[measurements-1]=last measure
            first = col[0]
            last = col[-1]
            if last == 1:
                detonations += 1
            elif np.any(col[:-1] == 1):
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        @qml.qnode(dev)
        def circuit():
            for i in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(qml.PauliZ(0))

        res = circuit()
        res = np.array(res)
        for s in res:
            if s == -1:  # PauliZ eigenvalue -1 => state |1>
                dud_predictions += 1
            else:
                live_predictions += 1
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
