# EVAL_META: task_id=41, framework=cirq, class=3
import cirq


def compose_op():
    return cirq.PauliString({0: cirq.Y, 1: cirq.I, 2: cirq.X})
