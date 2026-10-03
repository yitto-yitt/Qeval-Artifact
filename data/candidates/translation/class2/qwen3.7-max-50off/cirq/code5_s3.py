# EVAL_META: task_id=5, framework=cirq, class=2
import cirq

def create_state_prep():
    q = cirq.LineQubit.range(2)
    return cirq.Circuit(cirq.X(q[0]))
