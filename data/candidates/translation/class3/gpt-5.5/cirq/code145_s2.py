# EVAL_META: task_id=145, framework=cirq, class=3
import cirq

def qft_inverse(n):
    qubits = cirq.LineQubit.range(n)
    if n == 0:
        return cirq.Circuit()
    return cirq.Circuit(cirq.qft(*qubits, inverse=True))
