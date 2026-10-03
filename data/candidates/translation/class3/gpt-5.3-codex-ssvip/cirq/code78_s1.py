# EVAL_META: task_id=78, framework=cirq, class=3
import cirq


def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for j in range(num_qubits):
        q = qubits[j]
        for k in range(j):
            angle = -1 / (2 ** (j - k))
            circuit.append(cirq.CZPowGate(exponent=angle).on(qubits[k], q))
        circuit.append(cirq.H(q))
    return circuit
