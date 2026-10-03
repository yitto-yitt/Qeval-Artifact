# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits: int) -> cirq.Circuit:
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for i in range(num_qubits):
        for j in range(i):
            exponent = -1.0 / (2 ** (i - j))
            circuit.append(cirq.CZPowGate(exponent=exponent)(qubits[j], qubits[i]))
        circuit.append(cirq.H(qubits[i]))
    return circuit
