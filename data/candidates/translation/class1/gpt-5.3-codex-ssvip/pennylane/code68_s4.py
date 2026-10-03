# EVAL_META: task_id=68, framework=pennylane, class=1
import pennylane as qml
from numpy import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles

    if bomb_live:
        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for _ in range(shots):
            dev = qml.device("default.qubit", wires=1, shots=1)

            @qml.qnode(dev)
            def run_cycle():
                outcomes = []
                for _ in range(cycles):
                    qml.RY(e, wires=0)
                    outcomes.append(qml.sample(wires=0))
                outcomes.append(qml.sample(wires=0))
                return tuple(outcomes)

            result = run_cycle()
            bits = [int(r[0]) for r in result]

            if bits[0] == 1:
                detonations += 1
            elif 1 in bits[1:]:
                dud_predictions += 1
            else:
                live_predictions += 1
    else:
        dev = qml.device("default.qubit", wires=1, shots=shots)

        @qml.qnode(dev)
        def run_no_bomb():
            for _ in range(cycles):
                qml.RY(e, wires=0)
            return qml.sample(wires=0)

        samples = run_no_bomb()
        ones = int(samples.sum())
        zeros = shots - ones

        live_predictions = zeros
        dud_predictions = ones
        detonations = 0

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
