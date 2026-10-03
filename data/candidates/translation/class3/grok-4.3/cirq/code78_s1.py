# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.QuantumFourierTransformGate(num_qubits, without_reverse=True)
    inv_gate = gate ** -1
    return cirq.Circuit(inv_gate.on(*qubits))
