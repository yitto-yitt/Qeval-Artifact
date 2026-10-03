# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for j in range(num_qubits):
        for k in range(j):
            circuit.append(
                cirq.CZPowGate(exponent=-1 / (2 ** (j - k))).on(
                    qubits[j], qubits[k]
                )
            )
        circuit.append(cirq.H(qubits[j]))
    return circuit
