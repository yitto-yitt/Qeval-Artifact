# EVAL_META: task_id=6, framework=cirq, class=2
import cirq


def create_state_prep(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    if num_qubits == 0:
        return cirq.Circuit()
    ops = [cirq.I(q) for q in qubits]
    ops[-1] = cirq.X(qubits[-1])
    return cirq.Circuit(ops)
