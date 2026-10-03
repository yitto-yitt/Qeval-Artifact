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
            # A live bomb absorbs the |1> component; condition on survival.
            survival_probability *= float(state.probabilities()[0])
            state = Statevector.from_label("0")

    live_given_survival = float(state.probabilities()[0])
    if live_given_survival < 1e-15:
        live_given_survival = 0.0
    elif live_given_survival > 1.0 - 1e-15:
        live_given_survival = 1.0

    return {
        "live_predictions": survival_probability * live_given_survival,
        "dud_predictions": survival_probability * (1.0 - live_given_survival),
        "detonations": 1.0 - survival_probability,
    }
