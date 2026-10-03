# EVAL_META: task_id=68, framework=qiskit, class=1
from math import pi

from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Operator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    rotation = QuantumCircuit(1)
    rotation.ry(pi / cycles, 0)
    cycle_operator = Operator(rotation)
    survival_projector = Operator([[1, 0], [0, 0]])

    state = DensityMatrix.from_label("0")
    detonations = 0.0

    for _ in range(cycles):
        state = state.evolve(cycle_operator)
        if bomb_live:
            detonations += float(state.data[1, 1].real)
            state = state.evolve(survival_projector)

    probabilities = {
        "live_predictions": float(state.data[0, 0].real),
        "dud_predictions": float(state.data[1, 1].real),
        "detonations": detonations,
    }
    probabilities = {
        key: 0.0 if abs(value) < 1e-14 else max(0.0, value)
        for key, value in probabilities.items()
    }
    total = sum(probabilities.values())
    return {key: value / total for key, value in probabilities.items()}
