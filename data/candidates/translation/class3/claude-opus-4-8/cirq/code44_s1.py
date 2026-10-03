# EVAL_META: task_id=44, framework=cirq, class=3
import cirq


def tensor_circuits():
    top_q = cirq.LineQubit.range(1)
    top = cirq.Circuit()
    top.append(cirq.X(top_q[0]))

    bottom_q = cirq.LineQubit.range(2)
    bottom = cirq.Circuit()
    bottom.append(cirq.ry(0.2).on(bottom_q[1]).controlled_by(bottom_q[0]))

    n_top = len(top_q)
    n_bottom = len(bottom_q)
    tensored_qubits = cirq.LineQubit.range(n_bottom + n_top)

    tensored = cirq.Circuit()
    for op in bottom.all_operations():
        tensored.append(op.transform_qubits(
            {q: tensored_qubits[q.x] for q in op.qubits}))
    for op in top.all_operations():
        tensored.append(op.transform_qubits(
            {q: tensored_qubits[n_bottom + q.x] for q in op.qubits}))

    return tensored
