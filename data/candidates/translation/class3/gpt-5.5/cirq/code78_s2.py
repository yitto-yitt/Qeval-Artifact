# EVAL_META: task_id=78, framework=cirq, class=3
import cirq
import numpy as np

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for j in range(num_qubits):
        circuit.append(cirq.H(qubits[j]))
        for k in range(j + 1, num_qubits):
            circuit.append(cirq.CZPowGate(exponent=-1 / (2 ** (k - j))).on(qubits[j], qubits[k]))
    return circuit
