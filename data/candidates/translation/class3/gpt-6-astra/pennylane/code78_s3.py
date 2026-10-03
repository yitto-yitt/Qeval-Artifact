# EVAL_META: task_id=78, framework=pennylane, class=3
import pennylane as qml
from math import pi

def qft_no_swaps(num_qubits):
    with qml.tape.QuantumTape() as circuit:
        for j in range(num_qubits):
            for k in range(j):
                qml.ControlledPhaseShift(-pi / (2 ** (j - k)), wires=[j, k])
            qml.Hadamard(wires=j)
    return circuit
