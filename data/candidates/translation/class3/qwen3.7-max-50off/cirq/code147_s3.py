# EVAL_META: task_id=147, framework=cirq, class=3
import cirq

def mcy(qc):
    q0, q1, q2, q3, q4 = cirq.LineQubit.range(5)
    qc.append(cirq.Y(q4).controlled_by(q0, q1, q2, q3))
    return qc
