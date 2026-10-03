# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    for i in range(2):
        circuit.append(cirq.H(qubits[i + 1]), strategy=cirq.InsertStrategy.NEW)
    for i in range(2):
        circuit.append(cirq.CNOT(qubits[i + 1], qubits[i + 3]), strategy=cirq.InsertStrategy.NEW)
    return circuit ** -1
