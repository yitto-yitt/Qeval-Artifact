# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qft_gate = cirq.QuantumFourierTransformGate(num_qubits, without_reverse=True)
    inverse_qft_gate = qft_gate ** -1
    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(inverse_qft_gate.on(*qubits))
