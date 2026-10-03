# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(cirq.inverse(cirq.qft(*qubits, without_reverse=True)))
