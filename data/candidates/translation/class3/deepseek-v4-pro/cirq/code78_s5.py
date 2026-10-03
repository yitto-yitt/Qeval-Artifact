# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            circuit.append(cirq.CZPowGate(exponent=-1 / (2 ** (k - j))).on(qubits[k], qubits[j]))
        circuit.append(cirq.H(qubits[j]))
    return circuit
