# EVAL_META: task_id=90, framework=cirq, class=3
import cirq
import numpy as np

def create_custom_controlled():
    q = cirq.LineQubit.range(4)

    # Custom 2-qubit gate: X on target 0, H on target 1
    custom_unitary = np.kron(cirq.unitary(cirq.X), cirq.unitary(cirq.H))
    custom_gate = cirq.MatrixGate(custom_unitary)

    # Add two control qubits
    controlled_gate = custom_gate.controlled(2)

    circuit = cirq.Circuit()
    circuit.append(controlled_gate.on(q[0], q[3], q[1], q[2]))
    return circuit
