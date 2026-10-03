# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[1]).controlled_by(qubits[0], qubits[3]))
    circuit.append(cirq.H(qubits[2]).controlled_by(qubits[0], qubits[3]))
    return circuit
