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
        shots = 20000
        result = sim.run(qc, shots=shots).result()
        counts = result.get_counts()
        p1 = counts.get("1", 0) / shots
        p0 = counts.get("0", 0) / shots
        return {
            "live_predictions": 0.0,
            "dud_predictions": p1,
            "detonations": 0.0 + 0.0 * p0,
        }

    p_survive = (pow(__import__("math").cos(theta), 2)) ** cycles
    p_live = p_survive
    p_detonate = 1.0 - p_survive
    return {
        "live_predictions": p_live,
        "dud_predictions": 0.0,
        "detonations": p_detonate,
    }
