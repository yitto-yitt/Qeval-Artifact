# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for j in range(num_qubits):
        q = qubits[j]
        circuit.append(cirq.H(q))
        for k in range(j + 1, num_qubits):
            control = qubits[k]
            exponent = -1 / (2 ** (k - j))
            circuit.append(cirq.CZ(control, q) ** exponent)
    return circuit
