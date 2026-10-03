# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    qft_gate = cirq.QuantumFourierTransformGate(num_qubits, without_reverse=True)
    inv_qft_gate = qft_gate.inverse()
    return cirq.Circuit(inv_qft_gate.on(*qubits))
