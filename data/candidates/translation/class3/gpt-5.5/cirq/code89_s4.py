# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    q = cirq.LineQubit.range(3)
    return cirq.Circuit(cirq.H(q[2]).controlled_by(q[0], q[1]))
