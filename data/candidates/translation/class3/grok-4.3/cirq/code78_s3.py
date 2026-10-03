# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    qft_gate = cirq.QuantumFourierTransformGate(num_qubits=num_qubits, without_reverse=True)
    return cirq.Circuit((qft_gate**-1).on(*qubits))
