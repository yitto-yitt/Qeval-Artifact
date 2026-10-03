# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, Measure

def bell_dag():
    prog = QProg()
    prog << H(0) << CNOT(0, 1) << Measure(0, 0)
    return prog
