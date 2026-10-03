# EVAL_META: task_id=145, framework=cirq, class=3
import cirq

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    gate = cirq.QuantumFourierTransformGate(num_qubits=n)
    return cirq.Circuit(cirq.inverse(gate.on(*qubits)))
