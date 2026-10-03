# EVAL_META: task_id=0, framework=cirq, class=3
import cirq

def create_quantum_circuit(n_qubits):
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    if n_qubits > 0:
        circuit.append([cirq.I(q) for q in qubits])
    return circuit
