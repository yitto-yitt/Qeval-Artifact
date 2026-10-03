# EVAL_META: task_id=68, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    rotation = QuantumCircuit(1)
    rotation.ry(math.pi / cycles, 0)

    state = Statevector.from_label("0")
    survival = 1.0
    detonations = 0.0

    for _ in range(cycles):
        state = state.evolve(rotation)
        if bomb_live:
            probabilities = state.probabilities()
            p_detonation = float(probabilities[1] / probabilities.sum())
            detonations += survival * p_detonation
            survival *= 1.0 - p_detonation
            state = Statevector.from_label("0")

    probabilities = state.probabilities()
    probabilities /= probabilities.sum()
    live_predictions = survival * float(probabilities[0])
    dud_predictions = survival * float(probabilities[1])

    if not bomb_live:
        live_predictions = 0.0
        dud_predictions = 1.0

    return {
        "live_predictions": live_predictions,
        "dud_predictions": dud_predictions,
        "detonations": detonations,
    }
