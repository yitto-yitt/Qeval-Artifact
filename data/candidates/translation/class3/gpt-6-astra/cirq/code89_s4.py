# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q0, q1, q2 = cirq.LineQubit.range(3)
    return cirq.Circuit(cirq.H(q2).controlled_by(q0, q1))
