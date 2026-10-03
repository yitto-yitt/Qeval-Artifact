# EVAL_META: task_id=130, framework=cirq, class=3
import cirq

def inv_circuit(n):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append([
        cirq.CNOT(qubits[2], qubits[4]),
        cirq.CNOT(qubits[1], qubits[3]),
        cirq.H(qubits[2]),
        cirq.H(qubits[1])
    ])
    return circuit
