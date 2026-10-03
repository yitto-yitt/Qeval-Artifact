# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    for target in range(num_qubits - 1, -1, -1):
        for control in range(num_qubits - 1, target, -1):
            circuit.append(
                cirq.CZPowGate(exponent=-1 / (2 ** (control - target))).on(
                    qubits[control], qubits[target]
                )
            )
        circuit.append(cirq.H(qubits[target]))
    return circuit
