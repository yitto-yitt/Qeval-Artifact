# EVAL_META: task_id=23, framework=cirq, class=3
import cirq

def dj_constant_oracle():
    return cirq.Circuit(cirq.X(cirq.LineQubit(2)))
