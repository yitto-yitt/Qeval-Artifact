# EVAL_META: task_id=41, framework=cirq, class=3
import cirq

def compose_op():
    q0, q1, q2 = cirq.LineQubit.range(3)
    return cirq.PauliString({q0: cirq.Y, q1: cirq.I, q2: cirq.X})
