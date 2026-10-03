# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    qubits = [cirq.LineQubit(i) for i in range(5)]
    mcy_op = cirq.ControlledOperation(
        controls=qubits[:4],
        sub_operation=cirq.Y(qubits[4])
    )
    qc.append(mcy_op)
    return qc
