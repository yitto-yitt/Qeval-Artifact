# EVAL_META: task_id=0, framework=cirq, class=3
import cirq

def create_quantum_circuit(n_qubits):
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    circuit.append([], strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    for q in qubits:
        circuit.append(cirq.I(q))
    return circuit
