# EVAL_META: task_id=68, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = 3.141592653589793 / (2 * cycles)

    if not bomb_live:
        qc = QuantumCircuit(1, 1)
        for _ in range(cycles):
            qc.ry(2 * theta, 0)
        qc.measure(0, 0)

        sim = AerSimulator()
        result = sim.run(qc, shots=20000).result()
        counts = result.get_counts()
        p1 = counts.get("1", 0) / 20000.0
        p0 = counts.get("0", 0) / 20000.0
        return {
            "live_predictions": 0.0,
            "dud_predictions": p1,
            "detonations": p0,
        }

    p_survive = 1.0
    for _ in range(cycles):
        p_survive *= (1.0 - (theta ** 2))
    p_detonation = 1.0 - p_survive
    p_live = p_survive
    p_dud = 0.0

    return {
        "live_predictions": p_live,
        "dud_predictions": p_dud,
        "detonations": p_detonation,
    }
