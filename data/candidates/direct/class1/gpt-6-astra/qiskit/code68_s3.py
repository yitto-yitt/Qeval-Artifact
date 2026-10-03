# EVAL_META: task_id=68, framework=qiskit, class=1
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    rotation = QuantumCircuit(1)
    rotation.ry(pi / cycles, 0)

    state = Statevector.from_label("0")
    survival_probability = 1.0

    for _ in range(cycles):
        state = state.evolve(rotation)
        if bomb_live:
            probabilities = state.probabilities()
            no_detonation = float(
                probabilities[0] / sum(probabilities)
            )
            survival_probability *= no_detonation
            state = Statevector.from_label("0")

    if bomb_live:
        return {
            "live_predictions": survival_probability,
            "dud_predictions": 0.0,
            "detonations": 1.0 - survival_probability,
        }

    probabilities = state.probabilities()
    live_probability = float(probabilities[0] / sum(probabilities))
    if live_probability < 1e-15:
        live_probability = 0.0

    return {
        "live_predictions": live_probability,
        "dud_predictions": 1.0 - live_probability,
        "detonations": 0.0,
    }
