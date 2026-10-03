# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    custom = cirq.MatrixGate(
        np.kron(cirq.unitary(cirq.X), cirq.unitary(cirq.H))
    ).controlled(num_controls=2)
    return cirq.Circuit(custom.on(qubits[0], qubits[3], qubits[1], qubits[2]))
