# EVAL_META: task_id=90, framework=cirq, class=3
import numpy as np
import cirq

def create_custom_controlled():
    custom_gate = cirq.MatrixGate(
        np.kron(cirq.unitary(cirq.X), cirq.unitary(cirq.H))
    )
    controlled_gate = custom_gate.controlled(2)
    qubits = cirq.LineQubit.range(4)
    return cirq.Circuit(controlled_gate.on(qubits[0], qubits[3], qubits[1], qubits[2]))
