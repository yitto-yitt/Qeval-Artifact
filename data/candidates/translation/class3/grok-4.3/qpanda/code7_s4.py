# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import create_empty_circuit, qAlloc_many, RX, Parameter

def create_parametrized_gate():
    theta = Parameter("theta")
    prog = create_empty_circuit()
    q = qAlloc_many(1)
    prog.insert(RX(q[0], theta))
    return prog
