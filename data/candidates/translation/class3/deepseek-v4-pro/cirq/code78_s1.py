# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import math

def qft_no_swaps(num_qubits):
    """Return an inverse quantum Fourier transform circuit without swaps."""
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    # Inverse QFT without swaps: reverse order of forward QFT gates, each conjugated.
    for i in range(num_qubits - 1, -1, -1):
        for j in range(num_qubits - 1, i, -1):
            k = j - i
            exponent = -1.0 / (2 ** k)
            circuit.append(cirq.CZPowGate(exponent=exponent)(qubits[j], qubits[i]))
        circuit.append(cirq.H(qubits[i]))
    return circuit
