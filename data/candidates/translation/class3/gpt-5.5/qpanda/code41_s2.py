# EVAL_META: task_id=41, framework=qpanda, class=3
import pyqpanda3.core as pq


def compose_op():
    return pq.PauliOperator({"X0 Y2": 1.0})
