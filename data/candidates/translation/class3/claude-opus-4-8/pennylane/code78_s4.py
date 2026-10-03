# EVAL_META: task_id=78, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def qft_no_swaps(num_qubits):
    def _forward(wires):
        for j in reversed(range(num_qubits)):
            qml.Hadamard(wires=wires[j])
            for k in reversed(range(j)):
                lam = np.pi * (2.0 ** (k - j))
                qml.ControlledPhaseShift(lam, wires=[wires[j], wires[k]])

    def circuit(wires=None):
        if wires is None:
            wires = list(range(num_qubits))
        else:
            wires = list(wires)
        # inverse QFT without swaps = adjoint of forward QFT without swaps
        qml.adjoint(_forward)(wires)

    return circuit
