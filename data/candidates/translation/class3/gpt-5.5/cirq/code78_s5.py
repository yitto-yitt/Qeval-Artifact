# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for target in range(num_qubits):
        for control in range(target - 1, -1, -1):
            exponent = -1 / (2 ** (target - control))
            circuit.append((cirq.CZ ** exponent).on(qubits[control], qubits[target]))
        circuit.append(cirq.H(qubits[target]))
    return circuit
