# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for j in reversed(range(num_qubits)):
        for k in reversed(range(j + 1, num_qubits)):
            angle = -1.0 / (2 ** (k - j))
            circuit.append(cirq.CZ(qubits[j], qubits[k]) ** angle)
        circuit.append(cirq.H(qubits[j]))
    return circuit
