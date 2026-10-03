# EVAL_META: task_id=78, framework=cirq, class=3
import cirq

def qft_no_swaps(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    qft = cirq.qft(*qubits, without_reverse=True)
    return cirq.inverse(cirq.Circuit(qft))
