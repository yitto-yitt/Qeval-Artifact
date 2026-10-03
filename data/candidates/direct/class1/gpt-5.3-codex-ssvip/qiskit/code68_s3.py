# EVAL_META: task_id=68, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = 3.141592653589793 / (2 * cycles)

    if bomb_live:
        qc = QuantumCircuit(2, 2)
        qc.x(1)  # ancilla flag: 1 means not detonated so far

        for _ in range(cycles):
            qc.ry(2 * theta, 0)
            qc.cx(0, 1)

        qc.measure(0, 0)  # path qubit
        qc.measure(1, 1)  # ancilla flag (survival)

        sim = AerSimulator()
        shots = 200000
        counts = sim.run(qc, shots=shots).result().get_counts()

        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        for bitstr, c in counts.items():
            b0 = bitstr[-1]  # c0: path
            b1 = bitstr[-2]  # c1: ancilla/survival
            if b1 == "0":
                detonations += c
            else:
                if b0 == "0":
                    live_predictions += c
                else:
                    dud_predictions += c

        total = float(shots)
        return {
            "live_predictions": live_predictions / total,
            "dud_predictions": dud_predictions / total,
            "detonations": detonations / total,
        }

    qc = QuantumCircuit(1, 1)
    for _ in range(cycles):
        qc.ry(2 * theta, 0)
    qc.measure(0, 0)

    sim = AerSimulator()
    shots = 200000
    counts = sim.run(qc, shots=shots).result().get_counts()

    p0 = counts.get("0", 0) / shots
    p1 = counts.get("1", 0) / shots

    return {
        "live_predictions": 0.0,
        "dud_predictions": p1,
        "detonations": 0.0,
    }
