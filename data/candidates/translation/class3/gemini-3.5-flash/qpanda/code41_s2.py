# EVAL_META: task_id=41, framework=qpanda, class=3
import pyqpanda3.core as pq


def compose_op():
    return pq.PauliOperator({"Y2 X0": 1.0})
