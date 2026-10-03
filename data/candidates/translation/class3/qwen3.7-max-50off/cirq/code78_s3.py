# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for i in reversed(range(num_qubits)):
        for j in reversed(range(i + 1, num_qubits)):
            circuit.append(cirq.CZPowGate(exponent=-1 / 2**(j - i)).on(qubits[j], qubits[i]))
        circuit.append(cirq.H(qubits[i]))
    return circuit
