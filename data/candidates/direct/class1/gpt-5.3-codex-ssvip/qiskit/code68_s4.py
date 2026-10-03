# EVAL_META: task_id=68, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = 3.141592653589793 / (2 * cycles)

    qc = QuantumCircuit(2, 2)
    qc.x(1)  # arm qubit starts in |1> for interaction check

    for _ in range(cycles):
        qc.ry(2 * theta, 0)
        if bomb_live:
            qc.cx(0, 1)

    qc.measure(0, 0)
    qc.measure(1, 1)

    shots = 200000
    sim = AerSimulator()
    counts = sim.run(qc, shots=shots).result().get_counts()

    detonations = 0
    live_predictions = 0
    dud_predictions = 0

    for bitstr, c in counts.items():
        q1 = bitstr[0]
        q0 = bitstr[1]

        if bomb_live:
            if q1 == "0":
                detonations += c
            else:
                if q0 == "0":
                    live_predictions += c
                else:
                    dud_predictions += c
        else:
            if q0 == "1":
                dud_predictions += c
            else:
                live_predictions += c

    total = float(shots)
    return {
        "live_predictions": live_predictions / total,
        "dud_predictions": dud_predictions / total,
        "detonations": detonations / total,
    }
