# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, cast_qprog_to_qcircuit


def circ_to_gate(circ):
    if isinstance(circ, QProg):
        return cast_qprog_to_qcircuit(circ)
    return circ
