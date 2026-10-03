# EVAL_META: task_id=145, framework=cirq, class=3
import cirq

def qft_inverse(n):
    return cirq.qft(*cirq.LineQubit.range(n), inverse=True)
