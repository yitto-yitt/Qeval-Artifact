# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    qubits = cirq.LineQubit.range(3)
    return cirq.Circuit(
        cirq.ry(0.2).controlled_by(qubits[0])(qubits[1]),
        cirq.X(qubits[2])
    )
