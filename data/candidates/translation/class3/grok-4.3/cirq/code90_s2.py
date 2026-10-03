# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    xh_matrix = cirq.kron(cirq.unitary(cirq.X), cirq.unitary(cirq.H))
    custom_gate = cirq.MatrixGate(xh_matrix)
    controlled_custom = custom_gate.controlled(2)
    circuit.append(controlled_custom.on(qubits[0], qubits[3], qubits[1], qubits[2]))
    return circuit
