# EVAL_META: task_id=77, framework=pennylane, class=1
import math
import pennylane as qml


def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = [
        math.sqrt(probability_dist.get(basis_state, 0))
        for basis_state in range(2**num_qubits)
    ]
    wires = tuple(range(num_qubits))
    device = qml.device("default.qubit", wires=wires)

    @qml.qnode(device)
    def circuit():
        qml.StatePrep(amplitudes, wires=wires, normalize=False, validate_norm=True)
        return qml.probs(wires=wires)

    return circuit
