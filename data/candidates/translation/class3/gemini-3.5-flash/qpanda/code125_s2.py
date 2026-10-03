# EVAL_META: task_id=125, framework=qpanda, class=3
import pyqpanda3.core as pq


def circ_to_gate(circ):
    if isinstance(circ, pq.QProg):
        return pq.cast_qprog_to_qcircuit(circ)
    return circ
