# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    q = cirq.LineQubit.range(5)
    qc.append(cirq.Y.controlled(4).on(*q))
    return qc
